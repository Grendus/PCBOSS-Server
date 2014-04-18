import tornado.web
import Database
import Encryption

"""
The PCBOSS printer system only has a single point of entry.
This helps secure the web server against malicious users by obfuscating
the entry point.

All requests must pass the following values:
auth = the authorization code todo: replace the easy to type authorization code with a hash
type = the type of request. Current accepted methods are "add_user", "list_jobs",
"request_files", "update_job_status", "recent_files", "get_users", "edit_user".

Requests of type "add_user" must pass the following values:
email = the email address or user name of the user being registered. The system will try
    to alert the user at this address, so if it isn't a valid email address the user will
    not be alerted.
password = the desired password todo: hash the passwords
first_name = the users first name. Something has to be passed, even if it's a dummy value.
last_name = the users last name. Something has to be passed, even if it's a dummy value.

Requests of the type "list_jobs" do not need to pass any additional data.

Requests of the type "request_file" must pass the following values:
file_number = the number of a file on the server.

Requests of the type "update_job_status" must pass the following values:
file_number = the number of a file on th server.
status = the updated status value of the file

Requests of the type "recent_file" do not need to pass any additional data.

Requests of the type "recent_fie_timestamp" do not need to pass any additional data.

Requests of the type "get_users" do not need to send any additional data.

Requests of the type "update_user" must pass the following values:
email = the email address or user name of the user being registered. The system will try
    to alert the user at this address, so if it isn't a valid email address the user will
    not be alerted.
password = the desired password todo: hash the passwords
first_name = the users first name. Something has to be passed, even if it's a dummy value.
last_name = the users last name. Something has to be passed, even if it's a dummy value.
"""


class SystemRequestHandler(tornado.web.RequestHandler):
    def post(self):
        key = self.get_argument("key")
        data = self.get_argument("data")
        request = decryptEntrance({"key":key, "data":data})
        if request["auth"]=="PCBOSS":
            requestType = request["type"]
            if requestType == "add_user":
                email = request["email"]
                password = self.get_argument("password")
                first_name = request["first_name"]
                last_name = request["last_name"]
                if Database.addUser(email, Encryption.pwdHash(password), first_name, last_name):
                    self.write(Encryption.encryptEntrance("Success"))
                else:
                    self.write(Encryption.encryptEntrance("Failure"))
            elif requestType == "list_jobs":
                self.write(str(Encryption.encryptEntrance(Database.listJobs())))
            elif requestType == "request_file":
                filenum = request["file_number"]
                self.write(str(Encryption.encryptEntrance(Database.getJob(filenum))))
            elif requestType == "update_job_status":
                filenum = int(request["file_number"])
                status = request["status"]
                Database.updateStatus(filenum, status)
            elif requestType == "recent_file":
                self.write(str(Encryption.encryptEntrance(Database.mostRecentFile())))
            elif requestType == "recent_file_timestamp":
                self.write(str(Encryption.encryptEntrance(Database.mostRecentTimestamp())))
            elif requestType == "get_users":
                self.write(str(Encryption.encryptEntrance(Database.listUsers())))
            elif requestType == "edit_user":
                email = request["email"]
                fname = request["first_name"]
                lname = request["last_name"]
                pword = request["password"]
                Database.updateAccount(email, fname, lname, pword)
        else:
            self.write(Encryption.encryptEntrance("Error: Unrecognized Request"))

    def get(self):
        self.redirect("/")
            
