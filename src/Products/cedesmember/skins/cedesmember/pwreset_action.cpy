## Script (Python) "pwreset_action.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=randomstring, userid=None, password=None, password2=None
from Products.CMFCore.utils import getToolByName

status = "success"
pw_tool = getToolByName(context, 'portal_password_reset')
try:
    pw_tool.resetPassword(userid, randomstring, password)
    member= getToolByName(context, 'portal_membership').getMemberById(userid)
    # if a user has never logged in, the login time is set to 2000/01/01
    if member.getProperty('last_login_time','') == DateTime('2000/01/01'):
      if member.isCedesFree():
        status = "successfree"
      else:
        status = "success100pc"
except 'ExpiredRequestError':
    status = "expired"
except 'InvalidRequestError':
    status = "invalid"

return state.set(status=status)

