OperationalError
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2006, "MySQL server has gone away (ConnectionAbortedError(10053, 'An established connection was aborted by the software in your host machine', None, 10053, None))")
[SQL: SELECT users.id AS users_id, users.name AS users_name, users.email AS users_email, users.phone AS users_phone, users.department AS users_department, users.password_hash AS users_password_hash, users.`role` AS users_role, users.status AS users_status, users.created_at AS users_created_at, users.updated_at AS users_updated_at 
FROM users 
WHERE users.email = %(email_1)s 
 LIMIT %(param_1)s]
[parameters: {'email_1': 'admin@attendance.com', 'param_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/e3q8)

Traceback (most recent call last)
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 803, in _write_bytes
self._sock.sendall(data)
^^^^^^^^^^^^^^^^^^^^^^^^
During handling of the above exception, another exception occurred:
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
self.dialect.do_execute(
^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 951, in do_execute
cursor.execute(statement, parameters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
result = self._query(query)
         ^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
conn.query(q)
^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 557, in query
self._execute_command(COMMAND.COM_QUERY, sql)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 861, in _execute_command
self._write_bytes(packet)
^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 806, in _write_bytes
raise err.OperationalError(
^
The above exception was the direct cause of the following exception:
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 1478, in __call__
return self.wsgi_app(environ, start_response)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 1458, in wsgi_app
response = self.handle_exception(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 1455, in wsgi_app
response = self.full_dispatch_request()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 869, in full_dispatch_request
rv = self.handle_user_exception(e)
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 867, in full_dispatch_request
rv = self.dispatch_request()
     ^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\flask\app.py", line 852, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\app.py", line 143, in login
user = User.query.filter_by(email=email).first()
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2759, in first
return self.limit(1)._iter().first()  # type: ignore
       ^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2857, in _iter
result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                              
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2351, in execute
return self._execute_internal(
       
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2249, in _execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
                      
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
result = conn.execute(
         
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1419, in execute
return meth(
       
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 526, in _execute_on_connection
return connection._execute_clauseelement(
       
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1641, in _execute_clauseelement
ret = self._execute_context(
      
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
return self._exec_single_context(
       
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
self._handle_dbapi_exception(
^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2355, in _handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
self.dialect.do_execute(
^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 951, in do_execute
cursor.execute(statement, parameters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
result = self._query(query)
         ^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
conn.query(q)
^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 557, in query
self._execute_command(COMMAND.COM_QUERY, sql)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 861, in _execute_command
self._write_bytes(packet)
^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\etidi\OneDrive\Desktop\Attendance register\venv\Lib\site-packages\pymysql\connections.py", line 806, in _write_bytes
raise err.OperationalError(
^
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2006, "MySQL server has gone away (ConnectionAbortedError(10053, 'An established connection was aborted by the software in your host machine', None, 10053, None))")
[SQL: SELECT users.id AS users_id, users.name AS users_name, users.email AS users_email, users.phone AS users_phone, users.department AS users_department, users.password_hash AS users_password_hash, users.`role` AS users_role, users.status AS users_status, users.created_at AS users_created_at, users.updated_at AS users_updated_at
FROM users
WHERE users.email = %(email_1)s
LIMIT %(param_1)s]
[parameters: {'email_1': 'admin@attendance.com', 'param_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error.
To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

You can execute arbitrary Python code in the stack frames and there are some extra helpers available for introspection:

dump() shows all variables in the frame
dump(obj) dumps all that's known about the object
@echo off
title Attendance Portal - Fast Start
echo.
echo ========================================
echo   Starting Attendance Portal
echo ========================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo Starting application...
echo.
python start_fast.py
pause

