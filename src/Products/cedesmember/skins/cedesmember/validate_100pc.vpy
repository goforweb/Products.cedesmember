## Controlled Python Script "validate_100pc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates Cedes 100pc registration
##

request=context.REQUEST

# for robots
# compute is 3 x 4
if request.get("compute", "0") != "12":
  context.plone_utils.addPortalMessage(u"V\xe9rifiez le champ \"Combien font trois fois quatre?\" tout en bas du formulaire.", type="error")
  state.setError('compute', 'Il y a une erreur. Veuillez corriger.')

if request.get("extra_field", ""):
  state.setError('extra_field', 'Il y a une erreur. Veuillez corriger.')

#make sure chart is accepted
if not(request.get("legal_validation", False) == True):
  state.setError('legal_validation', 'Vous devez accepter la charte afin de pouvoir vous inscrire comme membre.')
  
if len(request.get("id")) > 32:
  state.setError('id', 'L\'identifiant ne peut dépasser 32 caractères. Veuillez corriger.')
  
# if request.get("email")!= None and request.get("email").find("hotmail") > 1:
#   state.setError('email', 'Pour des raisons techniques, nous ne pouvons actuellement pas accepter les boites hotmail. Veuillez entrez une autre adresse email.')
  
#if this is a cedes 100% inscription, make sure bill info is entered
if not(request.get("type", '') == 'free'):
  if not(request.get('bill_name', None)):
    state.setError('bill_name', 'Ce champ est obligatoire, veuillez le compléter.')
  if not(request.get('bill_email', None)):
    state.setError('bill_email', 'Ce champ est obligatoire, veuillez le compléter.')    
  if not(request.get('bill_country', None)):
    state.setError('bill_country', 'Ce champ est obligatoire, veuillez le compléter.')    
  if not(request.get('bill_address', None)):
    state.setError('bill_address', 'Ce champ est obligatoire, veuillez le compléter.')    
  if not(request.get('bill_postal_code', None)):
    state.setError('bill_postal_code', 'Ce champ est obligatoire, veuillez le compléter.')    
  if not(request.get('bill_locality', None)):
    state.setError('bill_locality', 'Ce champ est obligatoire, veuillez le compléter.')    
    
  if len(request.get("bill_name")) > 64:
    state.setError('bill_name', 'Ce champ ne peut dépasser 64 caractères. Veuillez corriger.')
  
  if len(request.get("bill_address")) > 64:
    state.setError('bill_address', 'Ce champ ne peut dépasser 64 caractères. Veuillez corriger.')
    
  if len(request.get("bill_postal_code")) > 64:
    state.setError('bill_postal_code', 'Ce champ ne peut dépasser 64 caractères. Veuillez corriger.')
  
  if len(request.get("bill_locality")) > 64:
    state.setError('bill_locality', 'Ce champ ne peut dépasser 64 caractères. Veuillez corriger.')
  
  # TVA validity
  if request.get("bill_tva"):                                          #Grèce is an exception to his rule
    if request.get("bill_tva")[0:2] != request.get("bill_country") and request.get("bill_tva")[0:2] != 'GR':
      state.setError('bill_tva', 'Votre numéro de TVA ne correspond pas au pays de l\'adresse de facturation. Veuillez entrer le numéro au complet en commençant par le code pays. Exemple pour la Belgique: BE0888923935.')
    elif context.check_tva_number(full_tva_num=request.get("bill_tva"))!= True:
      state.setError('bill_tva', 'Votre numéro de TVA n\'est pas valide. Veuillez entrer votre numéro sans espace en commençant par le code pays. Exemple pour la Belgique: BE0888923935.')

# validate email, another user with same email can not exist
email = request.get("email")
if email and not context.validate_registration_email(email):
    state.setError('email', 'Un compte est déjà lié à cette adresse e-mail.  Utilisez les procédures "Identifiant oublié?" et "Mot de passe oublié?" de la zone "Se connecter" pour récupérer votre identifiant et votre mot de passe.')

if state.getErrors():
  return state.set(status='failure',
                   portal_status_message='Veuillez corriger les erreurs indiquées.')

return state