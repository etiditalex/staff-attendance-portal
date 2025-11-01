"""
WebAuthn/FIDO2 utilities for biometric fingerprint authentication
Uses Web Authentication API for passwordless login
"""
import base64
import json
import secrets
from datetime import datetime
from flask import current_app, request, session, has_request_context
from models.db import WebAuthnCredential, db, User


def get_rp_id():
    """Get Relying Party ID from request"""
    hostname = request.host.split(':')[0]
    return hostname


def get_rp_name():
    """Get Relying Party name"""
    return "Staff Attendance Portal"


def get_origin():
    """Get origin URL"""
    scheme = request.scheme
    hostname = request.host
    return f"{scheme}://{hostname}"


def create_registration_options(user):
    """
    Create WebAuthn registration options for a user
    
    Args:
        user: User model instance
    
    Returns:
        dict: Registration options for browser WebAuthn API
    """
    # Get existing credentials
    existing_credentials = WebAuthnCredential.query.filter_by(user_id=user.id).all()
    exclude_credentials = [
        {
            "id": cred.credential_id,
            "type": "public-key",
            "transports": ["internal"]  # Platform authenticator (fingerprint)
        }
        for cred in existing_credentials
    ]
    
    # Generate challenge
    challenge = secrets.token_bytes(32)
    challenge_b64url = base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
    
    # Store challenge in session (use Flask session)
    # Flask sessions require a request context
    try:
        if 'webauthn_challenges' not in session:
            session['webauthn_challenges'] = {}
        session['webauthn_challenges'][str(user.id)] = base64.b64encode(challenge).decode('utf-8')
        session.permanent = True  # Make session persistent
    except RuntimeError:
        # Fallback if outside request context
        pass
    
    user_id_bytes = user.email.encode('utf-8')
    user_id_b64url = base64.urlsafe_b64encode(user_id_bytes).decode('utf-8').rstrip('=')
    
    # Create registration options
    options = {
        "challenge": challenge_b64url,
        "rp": {
            "name": get_rp_name(),
            "id": get_rp_id()
        },
        "user": {
            "id": user_id_b64url,
            "name": user.email,
            "displayName": user.name
        },
        "pubKeyCredParams": [
            {"type": "public-key", "alg": -7},  # ES256
            {"type": "public-key", "alg": -257}  # RS256
        ],
        "authenticatorSelection": {
            "authenticatorAttachment": "platform",  # Platform authenticator (fingerprint)
            "userVerification": "required",
            "requireResidentKey": False
        },
        "timeout": 60000,
        "attestation": "none",
        "excludeCredentials": exclude_credentials
    }
    
    return options


def verify_registration(user, credential_json, device_name=None):
    """
    Verify WebAuthn registration response
    
    Args:
        user: User model instance
        credential_json: Registration response from browser
        device_name: Optional device name
    
    Returns:
        tuple: (success: bool, credential_id or error: str)
    """
    try:
        # Get challenge from session
        try:
            challenge_b64 = session.get('webauthn_challenges', {}).get(str(user.id))
        except:
            challenge_b64 = None
        if not challenge_b64:
            return False, "Challenge not found in session"
        
        # Verify response structure
        if 'id' not in credential_json or 'response' not in credential_json:
            return False, "Invalid credential structure"
        
        credential_id = credential_json['id']
        
        # Check if credential already exists
        existing = WebAuthnCredential.query.filter_by(credential_id=credential_id).first()
        if existing:
            return False, "Credential already registered"
        
        # For now, accept the credential (in production, verify signature)
        # In a production environment, you should verify the attestation signature
        # This requires the webauthn library or cryptography library
        
        # Store credential
        credential = WebAuthnCredential(
            user_id=user.id,
            credential_id=credential_id,
            public_key=json.dumps(credential_json.get('response', {})),  # Store full response for now
            counter=0,
            device_name=device_name or request.user_agent.string[:100]
        )
        
        db.session.add(credential)
        db.session.commit()
        
        # Clean up challenge
        try:
            if 'webauthn_challenges' in session:
                session['webauthn_challenges'].pop(str(user.id), None)
        except:
            pass
        
        return True, credential_id
        
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def create_authentication_options(user_email):
    """
    Create WebAuthn authentication options for login
    
    Args:
        user_email: User email address
    
    Returns:
        tuple: (options: dict or None, error: str or None)
    """
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return None, "User not found"
    
    # Get user's credentials
    credentials = WebAuthnCredential.query.filter_by(user_id=user.id).all()
    if not credentials:
        return None, "No biometric credentials registered for this user"
    
    # Build allowCredentials list
    allow_credentials = [
        {
            "id": cred.credential_id,
            "type": "public-key",
            "transports": ["internal"]
        }
        for cred in credentials
    ]
    
    # Generate challenge
    challenge = secrets.token_bytes(32)
    challenge_b64url = base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
    
    # Store challenge in session
    try:
        if 'webauthn_auth_challenges' not in session:
            session['webauthn_auth_challenges'] = {}
        session['webauthn_auth_challenges'][user_email] = base64.b64encode(challenge).decode('utf-8')
        session.permanent = True
    except RuntimeError:
        pass
    
    # Create authentication options
    options = {
        "challenge": challenge_b64url,
        "timeout": 60000,
        "rpId": get_rp_id(),
        "allowCredentials": allow_credentials,
        "userVerification": "required"
    }
    
    return options, None


def verify_authentication(user_email, credential_json):
    """
    Verify WebAuthn authentication response
    
    Args:
        user_email: User email address
        credential_json: Authentication response from browser
    
    Returns:
        tuple: (success: bool, user or error: str)
    """
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return False, "User not found"
        
        # Get challenge from session
        try:
            challenge_b64 = session.get('webauthn_auth_challenges', {}).get(user_email)
        except:
            challenge_b64 = None
        if not challenge_b64:
            return False, "Challenge not found in session"
        
        # Find credential
        credential_id = credential_json.get('id')
        credential = WebAuthnCredential.query.filter_by(
            user_id=user.id,
            credential_id=credential_id
        ).first()
        
        if not credential:
            return False, "Credential not found"
        
        # For now, accept the authentication (in production, verify signature)
        # In a production environment, you should verify the signature using the public key
        
        # Update credential
        credential.counter = credential.counter + 1
        credential.last_used_at = datetime.utcnow()
        db.session.commit()
        
        # Clean up challenge
        try:
            if 'webauthn_auth_challenges' in session:
                session['webauthn_auth_challenges'].pop(user_email, None)
        except:
            pass
        
        return True, user
        
    except Exception as e:
        db.session.rollback()
        return False, str(e)
