from google.appengine.api import mail

SENDER_ADDRESS = "PathfinderPCBOSS@gmail.com"
COMPLETE_SUBJECT = "Your order is complete"
COMPLETE_BODY = "This is to inform you that your PCB order %s has been completed."

def sendComplete(fileinfo):
	mail.send_mail(SENDER_ADDRESS, fileinfo["submitter_name"], COMPLETE_BODY % fileinfo["filename"])