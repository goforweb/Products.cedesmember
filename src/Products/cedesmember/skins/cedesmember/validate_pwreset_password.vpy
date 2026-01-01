## Script (Python) "validate_password"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=userid=None, password=None, password2=None
##title=Validate password

#patch to fix password mismatch not checked
from Products.CMFPlone import PloneMessageFactory as _

failMessage = None

if not password:
  failMessage=_(u'Le mot de passe ne peut être vide')
elif len(password) < 5:
  failMessage=_(u'Votre mot de passe doit contenir au moins 5 caractères')
elif password2 is not None and password2 != password:
 failMessage=_(u'password_mismatch')

if failMessage:
  state.setError('password', failMessage) 
  
if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
