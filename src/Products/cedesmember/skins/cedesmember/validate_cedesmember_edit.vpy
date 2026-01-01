## Controller Python Script "validate_cedesmember_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validate cedesmember_edit_form contents
##

from Products.CMFPlone import PloneMessageFactory as _
request=context.REQUEST

#make sure chart is accepted
if not(request.get("legal_validation", False) == True):
  state.setError('legal_validation', 'Vous devez accepter la charte afin de pouvoir vous inscrire comme membre.')
  
#if this is a cedes 100% inscription, make sure bill info is entered
if not(context.isCedesFree()):
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
  

if state.getErrors():
  return state.set(status='failure',
                   portal_status_message='Veuillez corriger les erreurs indiquées.')

return state
