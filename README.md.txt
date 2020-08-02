# Research-Meta

- There are many papers available on internet for reference.
- 
 

### How it works?

- There two mobile applications - Present Me (for students) and Present Me Pro (for professors).
- There is one web portal.
- Now admin can use the web portal to add a person and assign them role (student or professor) manually or by just uploading CSV file.
- Now professor has to install Present Me Pro application and login with their credentials.
- Student has to install Present Me application and login with their credentials.
- Now, Professor will add lecture details and these details is sent to server.
- By encrypting this details, server give a token to Present Me Pro application, which will transfer that token with the help of Chirp.
- Students have to just keep open Present Me application.
- Present Me application receive the sound and chirp convert it into token (the one which was given by server to professor) again.
- This token is sent to server with student info.
- Server check the information of student and token decrypted by server.
- And with this an attendance of student marked into a system by server.


### Advantages

- Chirp generates very high pitch sound. So, in just 8-10 seconds, whole classroom's attendance (around 90-100 students') can be done by this system.
- This attendance can managed very easily by professor in the web portal.
- This is system is highly scalable and very secure.
- Professor can also mark attendance manually in the web portal, in case any student forgot the cell phone at home.


### Why this is so secure?

- Only admin can add the students and professors in system. Only admin can change or generate the password.
- When first time student login with his/her device, IMEI number of this device stored in database. (Admin can not see it and system encrypt it before storing). So, after first login, student does not need to login every time.
- Now suppose any student try to login with any other student's credentials, with the help of IMEI number both will be blocked by system.
- Only admin can unblock any blocked student.
- If any student purchase new device, only admin can add him/her.
- Present me application needs fingerprint of student in device to open.
- We have signed our applications and we are sending signed key with package and check on the server. So, if some one try to do reverse engineering and rebuild the application, system will detect it and block them to mark an attendane.
- We have used ProGuard, so reverse engineering is very defiicult. Other than this, we have encrypted variable names. This makes reverse engineering extreamly tough.
- Token used for mark attendance is encrypted by time stamp. So, students do not have time to record the audio and send it to other student for fake attendance.
- **Because we have encrypted variable names, code looks really dirty.**


### Build with

- Java
- [Chirp](https://github.com/chirp) - API for transfer data with sound
- [mysql](https://www.mysql.com/) - Database
- [Hibernate](https://hibernate.org/) - Java framework for simplifies application to interect with database
- [Spring](https://spring.io/) - Java Application Development Framework


### Demo

- Watch a [quick demo](https://drive.google.com/file/d/1X4Jkzv1MU37NBFuVUGwuuBEZYH0ey0Q4/view?t=08m29s)
- Watch a [full demo](https://drive.google.com/file/d/1X4Jkzv1MU37NBFuVUGwuuBEZYH0ey0Q4/view)


## Authors

* **Nirav C. Pansuriya**
* **Anuj H. Patel** 
