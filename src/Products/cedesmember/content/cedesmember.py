# -*- coding: UTF-8 -*-
# Copyright (c) 2007 Webin Concept (Brussels, BELGIUM).
# http://www.webinconcept.be -- webinconcept@gmail.com

##
# Cedes Member Content Type Based on Membrane and Remember
##

from Products.Archetypes import public as atapi
from Products.remember.content.member import Member as BaseMember
from Products.remember.permissions import EDIT_PROPERTIES_PERMISSION
from Products.cedesmember.config import DEFAULT_MEMBER_TYPE, PROJECTNAME, DEFAULT_PORTRAIT_DATA

from Products.cedes.config import COUNTRIES
from Products.cedes.widgets import TVAFieldWidget

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

from DateTime import DateTime
import httplib
import urllib
import urllib2
import base64
import hmac

# remplacer "cedes" par "cedestest"
BILL_APPLICATION_IDENTIFIER = "cedestest"
SHARED_KEY = "Kah942*$7sdp0)"
ACCOUNTING_APPLICATION_ROOT = 'www.unamur.be'
ACCOUNTING_APPLICATION_PATH = "/apps-factcedes/ext"

cedesmember_schema = atapi.Schema((
     atapi.StringField('teacher_number',
                               required=False,
                               regfield=False,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_teacher_number',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('member_type',
                               required=True,
                               regfield=True,
                               index='membrane_tool/FieldIndex',
                               vocabulary=["CeDES Free", "CeDES 100%"],
                               widget=atapi.SelectionWidget(
                                        format='radio',
                                        label_msgid='cedesmember_label_member_type',
                                        i18n_domain='cedesmember'),
            ),
    atapi.BooleanField('legal_validation',
                               regfield=True,
                               searchable=False,
                               widget = atapi.BooleanWidget(
                                        label = 'cedesmember_label_legal_validation',
                                        i18n_domain='cedesmember',
                                        macro='boolean_structured_label',
                                        render_own_label=True),
         ),
     atapi.StringField('lastname_married',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_lastname_married',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('firstname',
                               required=True,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_firstname',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('country',
                               required=True,
                               regfield=1,
                               default="BE",
                               vocabulary='listCountries',
                               widget=atapi.SelectionWidget(
                                        label_msgid='cedesmember_label_country',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('address',
                               required=True,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_address',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('postal_code',
                               required=True,
                               regfield=1,
                               index='membrane_tool/FieldIndex',
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_postal_code',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('locality',
                               required=True,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_locality',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('phone',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_phone',
                                        i18n_domain='cedesmember'),
            ),
     atapi.LinesField('network',
                               required=True,
                               regfield=1,
                               vocabulary=["Officiel", "Libre"],
                               widget=atapi.MultiSelectionWidget(
                                        format='checkbox',
                                        label_msgid='cedesmember_label_network',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('degree',
                               required=True,
                               regfield=1,
                               vocabulary=["Secondaire inferieur", "Secondaire superieur", "Superieur"],
                               widget=atapi.MultiSelectionWidget(
                                        format='checkbox',
                                        label_msgid='cedesmember_label_degree',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('section',
                               required=False,
                               regfield=1,
                               vocabulary=["General", "Transition technique", "Qualification", "Professionnel"],
                               widget=atapi.MultiSelectionWidget(
                                        description='A ne remplir que par les enseignants du secondaire',
                                        format='checkbox',
                                        label_msgid='cedesmember_label_section',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('school_name',
                               required=True,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_name',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('school_country',
                               required=True,
                               regfield=1,
                               vocabulary='listCountries',
                               default="BE",
                               widget=atapi.SelectionWidget(
                                        label_msgid='cedesmember_label_school_country',
                                        i18n_domain='cedesmember',),
           ),
     atapi.StringField('school_address',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_address',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('school_postal_code',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_postal_code',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('school_locality',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_locality',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('school_phone',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_phone',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('school_fax',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_fax',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('school_email',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_school_email',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('bill_tva',
                               required=False,
                               regfield=1,
                               widget=TVAFieldWidget(
                                        label_msgid='cedesmember_label_bill_tva',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('bill_email',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_bill_email',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('bill_name',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        description="Utilisez le format \"NOM prénom\" (par exemple DEMOULIN Emilie) ou le nom de l'institution en majuscules (par exemple UNAMUR)",
                                        label_msgid='cedesmember_label_bill_name',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('bill_country',
                               required=False,
                               regfield=1,
                               vocabulary='listCountries',
                               default="BE",
                               widget=atapi.SelectionWidget(
                                        label_msgid='cedesmember_label_bill_country',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('bill_address',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_bill_address',
                                        i18n_domain='cedesmember'),
            ),
     atapi.StringField('bill_postal_code',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_bill_postal_code',
                                        i18n_domain='cedesmember'),
           ),
     atapi.StringField('bill_locality',
                               required=False,
                               regfield=1,
                               widget=atapi.StringWidget(
                                        label_msgid='cedesmember_label_bill_locality',
                                        i18n_domain='cedesmember'),
           ),
     atapi.IntegerField('account_balance',
                               required=False,
                               default=0,
                               regfield=0,
                               widget=atapi.IntegerWidget(
                                        label_msgid='cedesmember_label_account_balance', visible = {'edit': 'invisible', 'view': 'invisible'},
                                        i18n_domain='cedesmember'),
            ),
     atapi.LinesField('account_transactions',
                               required=False,
                               default=[],
                               regfield=0,
                               widget=atapi.LinesWidget(
                                        label_msgid='cedesmember_label_account_transactions', visible = {'edit': 'invisible', 'view': 'invisible'},
                                        i18n_domain='cedesmember'),
            ),
     atapi.LinesField('account_bills',
                               required=False,
                               default=[],
                               regfield=0,
                               widget=atapi.LinesWidget(
                                        label_msgid='cedesmember_label_account_bills', visible = {'edit': 'invisible', 'view': 'invisible'},
                                        i18n_domain='cedesmember'),
            ),
    ),
)

basemember_schema = atapi.ManagedSchema(BaseMember.schema.copy().fields())
#basemember_schema['id'].widget.label_msgid = 'cedesmember_label_id'
#basemember_schema['email'].widget.label_msgid = 'cedesmember_label_email'
basemember_schema['fullname'].required = 1
basemember_schema['fullname'].widget.label_msgid = 'cedesmember_label_fullname'
basemember_schema['fullname'].widget.i18n_domain = 'cedesmember'
basemember_schema['fullname'].widget.description = ''

basemember_schema['portrait'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema['portrait'].default = DEFAULT_PORTRAIT_DATA
basemember_schema['location'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema['language'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema['make_private'].widget.visible = {'edit': 'visible', 'view': 'invisible'}
basemember_schema['title'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema['wysiwyg_editor'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}
basemember_schema.moveField('email', before='fullname')


class CedesMember(BaseMember):
    """A member with fields required for cedes subscription."""

    security = ClassSecurityInfo()
    archetype_name = portal_type = meta_type = DEFAULT_MEMBER_TYPE
    schema = basemember_schema + cedesmember_schema

    security.declarePublic('listCountries')
    def listCountries(self):
        """
           List available countries
        """
        vocab = []
        for country in COUNTRIES:
            vocab.append((country[0], country[1]))
        return atapi.DisplayList(tuple(vocab)).sortedByValue()

    def register(self):
        '''
          Calls BaseMember register method
          Sends email to notify administrator
          Asks a bill to buy credit if member 100%
        '''
        #calls base class method
        BaseMember.register(self)
        # send email to administrator
        mailHost = getToolByName(self, 'MailHost')
        skinsTool = getToolByName(self, 'portal_skins')
        email = skinsTool.cedesmember.mail_newmember_template(self.REQUEST)
        mailHost.send(email.encode('utf-8'))
        # asks for a bill
        if not(self.isCedesFree()):
            self.billCredits()

    def sendLogin(self):
        '''
          Sends email with login to the member
        '''
        # send email to member
        mailHost = getToolByName(self, 'MailHost')
        skinTool = getToolByName(self, 'portal_skins')
        email = skinTool.cedes_emails.login_reminder(self.REQUEST, member_email=self.email, member_id=self.id, firstname=self.getFirstname())
        mailHost.send(email.encode('utf-8'))

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'request100PC')
    def request100PC(self):
        '''
          Switch member to cedes 100%
        '''
        self.member_type = "CeDES 100%"
        self.reindexObject(idxs=['getMember_type',])
        self.billCredits()
        self.sendCedes100pcConfirmation()

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'requestCredit')
    def requestCredit(self):
        '''
          Request new credits - works only for CeDES 100% member
          Returns True if request proceed
        '''
        if self.isCedesFree():
            return False
        else:
            self.billCredits()
            #check if a Manager is renewing the subscription for a member
            #in this case, the current member id is different from the self.id
            currentUserId = self.portal_membership.getAuthenticatedMember().getId()
            if currentUserId == self.getId():
                self.sendCreditRequestConfirmation()
            return True

    security.declarePrivate('sendCedes100pcConfirmation')
    def sendCedes100pcConfirmation(self):
        '''
          Sends an email to confirm Cedes100pc request accepted
          Returns True if email has been sent
        '''
        skintool = getToolByName(self, 'portal_skins')
        mailHost = getToolByName(self, 'MailHost')
        email = skintool.cedes_emails.cedes100pc_request_confirmation(self.REQUEST, fullname=self.fullname, firstname=self.getFirstname(), member_email=self.email)
        mailHost.send(email.encode('utf-8'))
        return True

    def sendNoLoginNotification(self, now=DateTime(), days=3):
        '''
          Sends an email to notify the user that he has never logged in after 3 days
          Returns True if email has been sent
        '''
        #dont send notification if we have already send it within last d days
        # if a user has never logged in, the login time is set to 2000/01/01
        if not(hasattr(self, 'nologin_notification_date')) and self.getProperty('last_login_time','') == DateTime('2000/01/01'):
            registration_date = self.getRawCreation_date()
            #sends an email d days after registration
            if registration_date + days < now:
                #sends email
                skintool = getToolByName(self, 'portal_skins')
                mailHost = getToolByName(self, 'MailHost')
                email = skintool.cedes_emails.registration_nologin_notification(self.REQUEST, fullname=self.fullname, firstname=self.getFirstname(), member_email=self.email)
                mailHost.send(email.encode('utf-8'))
                #marks member that notification has been sent
                self.nologin_notification_date = now
                return True
        return False

    security.declarePrivate('sendCreditRequestConfirmation')
    def sendCreditRequestConfirmation(self):
        '''
          Sends an email to confirm Credit request accepted
          Returns True if email has been sent
        '''
        skintool = getToolByName(self, 'portal_skins')
        mailHost = getToolByName(self, 'MailHost')
        email = skintool.cedes_emails.credit_request_confirmation(self.REQUEST, fullname=self.fullname, firstname=self.getFirstname(), member_email=self.email)
        mailHost.send(email.encode('utf-8'))
        return True

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'addTransaction')
    def addTransaction(self, articleUID, articlePrice=1, isDossierStructure=False):
        '''
          Adds a transaction : (UID, price, date)
          Does not check the balance
          Sends a notification by email if credit passes below 20
          Returns None
          articlePrice can be 0 if we are registering transactions for ArticlePayant of a DossierStructure
        '''
        if not("Manager" in self.getRoles()):
            #an article is payed once then accessed
            #but for DossierStructure, if it has been updated, the price is adapted and
            #the pdf is no more accessible
            if not isDossierStructure and self.checkViewable(articleUID):
                return None
            previous_balance = self.account_balance
            self.account_balance -= articlePrice
            if previous_balance >= 20 and self.account_balance < 20:
                self.sendLowReminder()
            self.account_transactions = self.account_transactions + ((articleUID, articlePrice, DateTime()),)
        return None

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'checkViewable')
    def checkViewable(self, articleUID):
        """
          Check if the article can still be viewed.  An element is viewable when his UID is found in member transactions
        """
        if not("Manager" in self.getRoles()):
            inversed_transactions = tuple(reversed(self.account_transactions))
            for trUID, trPrice, trDate in inversed_transactions:
                if trUID == articleUID:
                    #we found (maybe) the last time the element was accessed
                    #check if it was accessed less than 1 day ago
                    #if trDate > DateTime() - 1:
                    #    return trDate + 1
                    return True
        else:
            return True
        return False

    security.declarePrivate('sendLowReminder')
    def sendLowReminder(self):
        '''
          Sends a notification email with credit information
          Returns True if email has been sent
        '''
        skintool = getToolByName(self, 'portal_skins')
        mailHost = getToolByName(self, 'MailHost')
        email = skintool.cedes_emails.credit_low_notification(self.REQUEST, fullname=self.fullname, firstname=self.firstname, member_email=self.email, balance = self.getBalance())
        mailHost.send(email.encode('utf-8'))
        return True

    security.declareProtected(permissions.ManagePortal, 'addBill')
    def addBill(self, bill_id, price=3000, mode='F', date=None, payment_date=None):
        '''
          Adds a bill : {bill_id, price, mode, date, payment_date}
          param bill_id id of the bill generated by FUNDP accounting
          param price  price as integer : 3000 stands for 30,00 euros
          param mode   "F" (facture) or "N" (note de crédit)
          param date   date of the bill
          param payment_date date when payment has been validated
          Returns None
        '''
        #if not("Manager" in self.getRoles()):
        date = date or DateTime()
        self.account_bills = self.account_bills + ({'bill_id':bill_id, 'price':price, 'mode':mode, 'date':date, 'payment_date':payment_date},)

    security.declareProtected(permissions.ManagePortal, 'sendExpirationReminder')
    def sendExpirationReminder(self, now=DateTime(), days=14):
        '''
          Sends Expiration email reminder if credit expires in 14 days
          Returns True if email sent, False otherwise
        '''
        if not(self.isCedesFree()) and not("Manager" in self.getRoles()):
            expiration_date = self.getExpirationDate()
            #sends an email d days before only if the credits are not already expired!!!
            if expiration_date and expiration_date - days < now and not expiration_date < now:
                #dont send notification if we have already send it within last d days
                if not(hasattr(self, 'expiration_notification_date') and self.expiration_notification_date > now - days):
                    #sends email
                    skintool = getToolByName(self, 'portal_skins')
                    mailHost = getToolByName(self, 'MailHost')
                    email = skintool.cedes_emails.credit_expiration_notification(self.REQUEST, fullname=self.fullname, firstname=self.firstname, member_email=self.email, expiration_date = expiration_date)
                    mailHost.send(email.encode('utf-8'))
                    #marks member that notification has been sent
                    self.expiration_notification_date = now
                    return True
        return False

    security.declareProtected(permissions.ManagePortal, 'sendPaymentReminder')
    def sendPaymentReminder(self, now=DateTime(), days=10):
        '''
          Sends a payment reminder email if payment has not been made last 10 days
          Returns True if email sent, False if there was an error getting the bill
          in the accounting application or None if nothing to do
        '''
        if not(self.isCedesFree()) and not("Manager" in self.getRoles()):
            if self.getBillWaitingPayment():
                waiting_payment_date = self.getBillWaitingPayment()['date']
                # sends an email d days after
                if now > waiting_payment_date + days:
                    # dont send notification if we have already sent
                    if not(hasattr(self, 'payment_notification_date')):
                        #sends email with bill duplicata as attachment
                        bill_waiting_payment = self.getBillWaitingPayment()
                        bill_id = bill_waiting_payment['bill_id']
                        bill = self._getBill(bill_id) or bill_waiting_payment.get('pdf', None)
                        if not bill:
                            return False
                        skintool = getToolByName(self, 'portal_skins')
                        mailHost = getToolByName(self, 'MailHost')
                        from email.mime.multipart import MIMEMultipart
                        from email.mime.base import MIMEBase
                        from email.mime.text import MIMEText
                        from email import Encoders
                        msg = MIMEMultipart()
                        msg['Subject'] = 'CeDES - Votre paiement en attente'
                        msg['From'] = '%s <%s>' % (skintool.email_from_address, skintool.email_from_name)
                        msg['To'] = '%s %s <%s>' % (self.fullname, self.firstname, self.email)
                        body = MIMEText(skintool.cedes_emails.credit_payment_notification(self.REQUEST,
                                                                                          firstname=self.firstname).encode('utf-8'),
                                        'plain', 'utf-8')
                        attachment = MIMEBase('application', 'pdf')
                        attachment.set_payload(bill)
                        Encoders.encode_base64(attachment)
                        attachment.add_header('Content-Disposition', 'attachment', filename='facture.pdf')
                        msg.attach(body)
                        msg.attach(attachment)
                        mailHost.send(msg)
                        #marks member that notification has been sent
                        self.payment_notification_date = now
                        return True
        return None

    def _getBill(self, bill_id):
        """
          Get the bill from accounting application
        """
        try:
            conn = urllib2.urlopen('https://%s%s/print?bill_num=%s&bill_application=%s' % (ACCOUNTING_APPLICATION_ROOT,
                                                                                     ACCOUNTING_APPLICATION_PATH,
                                                                                     bill_id,
                                                                                     BILL_APPLICATION_IDENTIFIER))
            if conn.code != 200:
                return None
            facture = conn.fp.read()
            return facture
        except:
            return None

    security.declareProtected(permissions.ManagePortal, 'cancel100PC')
    def cancel100PC(self, now=DateTime(), days=30):
        '''
          Switch member to cedes free if never paid 30 days later, and his balance is 0
          deletes the payment_notification_date variable
          Sends a credit note to accounting
          Returns True if credit note was sent, False otherwise
        '''
        if not(self.isCedesFree()) and not("Manager" in self.getRoles()):
            if self.getBillWaitingPayment():
                waiting_payment_date = self.getBillWaitingPayment()['date']
                if now >  waiting_payment_date + days:
                    #sets member to free only if his balance is zero
                    if self.getBalance()<=0:
                        self.member_type = "CeDES Free"
                    if hasattr(self, 'payment_notification_date'):
                        del self.payment_notification_date
                    # if len(self.account_bills)>0:
                    #   last_bill = self.account_bills[-1]
                    self.billCredits(total=self.getBillWaitingPayment()['price'], mode="N")
                    self.reindexObject()
                    return True
        return False

    security.declareProtected(permissions.ManagePortal, 'credit')
    def credit(self, value):
        '''
          Credit the account
          Sends credit activation email
        '''
        self.account_balance += value
        self.account_transactions = self.account_transactions + (('crédit', value, DateTime()),)
        #sends email notification
        skintool = getToolByName(self, 'portal_skins')
        mailHost = getToolByName(self, 'MailHost')
        email = skintool.cedes_emails.credit_activation_notification(self.REQUEST, member_email=self.email, firstname=self.firstname, credit=value)
        mailHost.send(email.encode('utf-8'))

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'resetCredit')
    def resetCredit(self):
        '''Sets the balance to zéro and adds the transaction information'''
        self.account_transactions = self.account_transactions + (('expiration du crédit', self.account_balance, DateTime()),)
        self.account_balance -= self.account_balance

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'resetExpiredCredit')
    def resetExpiredCredit(self, now=DateTime()):
        '''
          Reset credit of member if it has expired
          Returns 2 if credit was reset, 1 if credits reset and member set to "CeDES Free" and 0 if nothing is done...
        '''
        if not(self.isCedesFree()) and not("Manager" in self.getRoles()):
            if self.getLastPaymentDate() and self.getExpirationDate() < now:
                self.resetCredit()
                #!!! set the member to Free if his credits have expired and no bill is waiting payment !!!
                if not self.getBillWaitingPayment():
                    self.member_type = "CeDES Free"
                    self.reindexObject(idxs=['getMember_type',])
                    #send a mail to the member to warn him...
                    skintool = getToolByName(self, 'portal_skins')
                    mailHost = getToolByName(self, 'MailHost')
                    email = skintool.cedes_emails.credit_expired_notification(self.REQUEST, fullname=self.fullname, firstname=self.firstname, member_email=self.email, expiration_date = self.getExpirationDate())
                    mailHost.send(email.encode('utf-8'))
                    return 1
                return 2
        return 0

    security.declareProtected(permissions.ManagePortal, 'validatePayment')
    def validatePayment(self, now=DateTime()):
        '''
          Validates the payment
          Adds the current date to last item of account_bills
          Removes the 'payment_notification_date' variable (used to send payment reminder)
          Removes the 'expiration_notification_date' variable (used to send expiration)
          Returns True if waiting payment was validated, False otherwise
        '''
        if self.getBillWaitingPayment():
            self.account_bills[-1]['payment_date'] = now
            if hasattr(self, 'payment_notification_date'):
                del self.payment_notification_date
            if hasattr(self, 'expiration_notification_date'):
                del self.expiration_notification_date
            self.reindexObject()
            return True
        return False

    security.declareProtected(permissions.ManagePortal, 'hasFailedAccountingF')
    def hasFailedAccountingF(self):
        '''
          Returns True if there was a problem during accounting a 'F' and so
          a 'bill_accounting_failed' is set on the member.
        '''
        if hasattr(self, 'bill_accounting_failed') and \
           self.bill_accounting_failed is not None and \
           self.bill_accounting_failed[1] == 'F':
                return True
        return False

    security.declareProtected(permissions.ManagePortal, 'hasFailedAccountingN')
    def hasFailedAccountingN(self):
        '''
          Returns True if there was a problem during accounting a 'N' and so
          a 'bill_accounting_failed' is set on the member.
        '''
        if hasattr(self, 'bill_accounting_failed') and \
           self.bill_accounting_failed is not None and \
           self.bill_accounting_failed[1] == 'N':
                return True
        return False

    security.declareProtected(permissions.ManagePortal, 'cancelFailedAccounting')
    def cancelFailedAccounting(self, bill_id):
        '''
          Cancel a failed accounting, turn the failed bill into a correct bill
          with a special id 'no_bill_id_failed_accounting_managed_manually'.
        '''
        if hasattr(self, 'bill_accounting_failed') and self.bill_accounting_failed is not None:
            if not bill_id:
                bill_id = 'no_bill_id_failed_accounting_managed_manually'
            self.addBill(bill_id,
                         self.bill_accounting_failed[0],
                         self.bill_accounting_failed[1],
                         self.bill_accounting_failed[2], )
            del self.bill_accounting_failed
        self.reindexObject()

    security.declareProtected(permissions.ManagePortal, 'removeFailedAccounting')
    def removeFailedAccounting(self):
        '''
          Just remove the marker of a failed accounting.
        '''
        if hasattr(self, 'bill_accounting_failed') and self.bill_accounting_failed is not None:
            del self.bill_accounting_failed
            self.reindexObject()

    security.declareProtected(permissions.ManagePortal, 'retryBillCredits')
    def retryBillCredits(self):
        '''
          Tries to rebill credits if previous attempt failed
          Returns True if successfull, False otherwise
          None if member was not waiting to send a bill
        '''
        if hasattr(self, 'bill_accounting_failed') and self.bill_accounting_failed is not None:
            return self.billCredits(total=self.bill_accounting_failed[0], mode=self.bill_accounting_failed[1])
        else:
            return None

    ##
    # Request new credits. By default, request is 30 euros.
    # Connects to accounting application and sends user information
    # La réponse (text/plain) envoyée par l'application comptable est composée de 1 ou 2 lignes comme suit :
    # return=x
    # facture=y
    #
    # x peut prendre les valeurs suivantes :
    # 0 : tout OK ; la deuxième ligne est présente
    # 1 : la facture est enregistrée mais le serveur a rencontré une erreur dans la génération du PDF ; la deuxième ligne est présente
    # 2 : la facture est enregistrée mais le serveur a rencontré une erreur lors de l'envoi du mail ; la deuxième ligne est présente
    # 10 : erreur interne de l'application ; pas de deuxième ligne
    # 11 : l'application (bill_application) est inconnue ; pas de deuxième ligne
    # 12 : le digest n'est pas correct ; pas de deuxième ligne
    # 13 : erreur lors de l'enregistrement de l'abonné ; pas de deuxième ligne
    #
    # y est le numéro de facture attribué par la comptabilité des FUNDP et devra servir au CeDES à associer les paiements reçus avec les demandes d'abonnement.
    #
    # If transaction not successfull, stores bill information to retry later in 'bill_accounting_failed' variable
    # If transaction successfull, stores bill information by adding a new bill to the account_bills variable
    # @param total amount in euros to bill
    # @param mode F if total to bill (facture), N if total to credit (note de crédit)
    # @returns True if transaction successfull, False otherwise
    ##
    security.declarePrivate('billCredits')
    def billCredits(self, total="3000", mode="F"):
        '''Bill credits and contact bill application'''

        #encode in utf-8 all parameters
        #change the following line with cedestest if you want to test
        bill_application = unicode(BILL_APPLICATION_IDENTIFIER).encode("utf-8")
        bill_id = unicode(self.id).encode("utf-8")
        bill_name = unicode(self.bill_name).encode("utf-8")
        bill_country = unicode(self.bill_country).encode("utf-8")
        bill_address = unicode(self.bill_address).encode("utf-8")
        bill_postal_code = unicode(self.bill_postal_code).encode("utf-8")
        bill_locality = unicode(self.bill_locality).encode("utf-8")
        if mode == "F":
            connectedMember = self.portal_membership.getAuthenticatedMember()
            if not connectedMember.getId() == self.getId():
                #a Manager is renewing the credits for the user
                #take his e-mail address instead of the user's one
                if hasattr(connectedMember, 'bill_email'):
                    bill_email = unicode(connectedMember.bill_email).encode("utf-8")
                else:
                    #a new member is registering
                    bill_email = unicode(self.bill_email).encode("utf-8")
            else:
                bill_email = unicode(self.bill_email).encode("utf-8")
        else:
            #Note de credits are only sent to cedes@unamur.be
            bill_email = 'cedes@unamur.be'
        bill_tva = unicode(self.bill_tva).encode("utf-8")
        if bill_tva == '':
            bill_tva = 'N/A'
        bill_amount_htva = unicode(total).encode("utf-8")
        bill_type = unicode(mode).encode("utf-8")

        #calculates HMAC digest
        hm = hmac.new(SHARED_KEY)
        hm.update(bill_application)
        hm.update(bill_id)
        hm.update(bill_name)
        hm.update(bill_country)
        hm.update(bill_address)
        hm.update(bill_postal_code)
        hm.update(bill_locality)
        hm.update(bill_email)
        hm.update(bill_tva)
        hm.update(bill_amount_htva)
        hm.update(bill_type)
        bill_digest = base64.encodestring(hm.digest()).strip()

        # notify accounting application of a new user
        headers = {"Content-type": "application/x-www-form-urlencoded; charset=utf-8",
                   "Accept": "text/plain;",
                   "accept-charset":"utf-8",}

        #url encodes all parameters
        params = urllib.urlencode({'bill_application' : bill_application,
                               'bill_id':bill_id,
                               'bill_name': bill_name,
                               'bill_country': bill_country,
                               'bill_address': bill_address,
                               'bill_postal_code': bill_postal_code,
                               'bill_locality': bill_locality,
                               'bill_email' : bill_email,
                               'bill_tva': bill_tva,
                               'bill_amount_htva':bill_amount_htva,
                               'bill_type': bill_type,
                               'bill_digest': bill_digest})

        #connects to accounting application
        now=DateTime()
        try:
            conn = httplib.HTTPSConnection(ACCOUNTING_APPLICATION_ROOT)
            #conn.set_debuglevel(1)
            conn.request("POST", ACCOUNTING_APPLICATION_PATH, params, headers)
            response = conn.getresponse()
            if response.status != 200:
                #If server is not up and ready, try later
                self.bill_accounting_failed = (total, mode, now)
                self.reindexObject(idxs=['hasFailedAccounting'])
                skinTool = getToolByName(self, 'portal_skins')
                mailHost = getToolByName(self, 'MailHost')
                error_text = "SERVEUR INDISPONIBLE, L'application Cedes tentera de se reconnecter à l'application comptable plus tard."
                email = skinTool.cedes_emails.registration_error_manager(self.REQUEST, member_id=bill_id, error_text=error_text)
                mailHost.send(email.encode('utf-8'))
                return False

            originaldata = response.read()
            data = originaldata.split('\n')
            #print data
            x = data[0].strip().strip('return=')
            y = None
            if x == '0' or x == '1' or x == '2':
                y = data[1].strip().strip('facture=')

            # if bill was ok
            if x == '0':
                # F or N mode does not change anything
                self.addBill(y, price=total, mode=mode, date=now, payment_date=None)
                if hasattr(self, 'bill_accounting_failed'):
                    del self.bill_accounting_failed
                return True
            else:
                #traiter tous les cas d'erreur avec email à l'administrateur.
                if y is None:
                    #Pas de facture générée, try later
                    self.bill_accounting_failed = (total, mode, now)
                    self.reindexObject(idxs=['hasFailedAccounting'])
                #envoi d'un email à administrateur pour signifier l'erreur
                skinTool = getToolByName(self, 'portal_skins')
                mailHost = getToolByName(self, 'MailHost')
                email = skinTool.cedes_emails.registration_error_manager(self.REQUEST, member_id=bill_id, error_text=originaldata)
                mailHost.send(email.encode('utf-8'))
                return False
        except:
          #If connection failed, try later
          self.bill_accounting_failed = (total, mode, now)
          self.reindexObject(idxs=['hasFailedAccounting'])
          skinTool = getToolByName(self, 'portal_skins')
          mailHost = getToolByName(self, 'MailHost')
          import sys
          error_text = sys.exc_info()
          email = skinTool.cedes_emails.registration_error_manager(self.REQUEST, member_id=bill_id, error_text=error_text)
          mailHost.send(email.encode('utf-8'))
          return False

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'getTransactions')
    def getTransactions(self):
        '''Returns list of transactions'''
        return self.account_transactions

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'getBalance')
    def getBalance(self):
        '''Returns balance'''
        return self.getAccount_balance()

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'getLastPaymentDate')
    def getLastPaymentDate(self):
        '''
          Returns the Date of the last time the account payment was validated.
          Returns None if the account was never credited
        '''
        if self.account_bills:
            bill_reversed = tuple(reversed(self.account_bills))
            for item in bill_reversed:
                if item['payment_date']!=None and item['mode'] == "F": return item['payment_date']
        return None

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'getBillWaitingPayment')
    def getBillWaitingPayment(self):
        '''
          Returns bill_id of the bill waiting for a payment
          Returns None if no bill is waiting for payment
        '''
        if len(self.account_bills) > 0:
            item = self.account_bills[-1]
            if item['payment_date']==None and item['date'] !=None and item['mode']=='F': return item
        return None

    security.declareProtected(permissions.ManagePortal, 'hasBillWaitingPayment')
    def hasBillWaitingPayment(self):
        """Does current member has a bill waiting payment?"""
        return bool(self.getBillWaitingPayment())

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'getExpirationDate')
    def getExpirationDate(self):
        '''
          Returns the expiration date (last payment date + 365 days).
          Returns None if the account was never credited.
        '''
        lpd = self.getLastPaymentDate()
        if lpd is not None:
            return lpd + 365
        return None

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'checkBalance')
    def checkBalance(self, price):
        '''
          Checks if we can afford a purchase's price
          Returns True if balance > price, False otherwise
        '''
        #the balance of a manager is always ok
        if "Manager" in self.getRoles():
            return True
        if self.getBalance() - price >= 0:
            return True
        else:
            return False

    security.declareProtected(EDIT_PROPERTIES_PERMISSION, 'isCedesFree')
    def isCedesFree(self):
        '''Returns True if member is a CeDES Free member Type, False otherwise'''
        if self.member_type == "CeDES Free":
            return True
        else:
            return False

    def validate_registration_email(self, email):
        """Used during registration, a user can not register if email already in use."""
        email = email.strip()
        # some domains may create several accounts
        BYPASSED_DOMAINS = ['@unamur.be', '@goforweb.be', '@fundp.ac.be']
        for domain in BYPASSED_DOMAINS:
            if domain in email:
                return True
        mTool = getToolByName(self, 'portal_membership')
        return not bool(mTool.searchForMembers(email=email))

    #security.declarePublic('validate_legal_validation')
    #def validate_legal_validation(self, value):
    #    '''Validate the content of the 'legal_validation' field'''
    #    # Strangely, the default validator fails...
    #    if not value == True:
    #        return 'Vous devez accepter la charte afin de pouvoir vous inscrire comme membre.'
    #
    #security.declarePublic('validate_bill_name')
    #def validate_bill_name(self, value):
    #    '''Validate the content of the 'bill_name' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'
    #
    #security.declarePublic('validate_bill_email')
    #def validate_bill_email(self, value):
    #    '''Validate the content of the 'bill_email' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'
    #
    #security.declarePublic('validate_bill_country')
    #def validate_bill_country(self, value):
    #    '''Validate the content of the 'bill_country' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'
    #
    #security.declarePublic('validate_bill_address')
    #def validate_bill_address(self, value):
    #    '''Validate the content of the 'bill_address' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'
    #
    #security.declarePublic('validate_bill_postal_code')
    #def validate_bill_postal_code(self, value):
    #    '''Validate the content of the 'bill_postal_code' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'
    #
    #security.declarePublic('validate_bill_locality')
    #def validate_bill_locality(self, value):
    #    '''Validate the content of the 'bill_locality' field'''
    #    # If member_type is "CeDES 100%" this field is mandatory
    #    if not value and not self.isCedesFree():
    #        return 'Ce champ est obligatoire, veuillez le compléter.'


atapi.registerType(CedesMember, PROJECTNAME)


# #URL encode method
# def notifyTest(self):
#     #notify accounting application of a new user
#     headers = {"Content-type": "application/x-www-form-urlencoded;",
#                "Accept": "text/plain;"}
#
#     params = urllib.urlencode({'sender_fullname': 'Tony silva',
#                                'sender_from_address': 'webinconcept@gmail.com',
#                                'subject': 'le sujet',
#                                'message': 'le message',
#                                'form.submitted':1})
#     try:
#       conn = httplib.HTTPConnection('cedes4.webinconcept.be')
#       #con.set_debuglevel(1)
#       conn.request("POST", "/contact-info", params, headers)
#       response = conn.getresponse()
#       print response.status, response.reason
#       data = response.read()
#       conn.close()
#       return data
#     except:
#       return 'ERROR: could not connect to accounting server'

# #multipart method
# #http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
# import httplib, mimetypes
# #updated with HTTPConnection ; removed file support
# def post_multipart(host, selector, fields):
#     content_type, body = encode_multipart_formdata(fields)
#     h = httplib.HTTPConnection(host)
#     headers = {
#         'User-Agent': 'INSERT USERAGENTNAME',
#         'Content-Type': content_type
#         }
#     h.request('POST', selector, body, headers)
#     res = h.getresponse()
#     return res.status, res.reason, res.read()
#
# def encode_multipart_formdata(fields):
#     """
#     fields is a sequence of (name, value) elements for regular form fields.
#     files is a sequence of (name, filename, value) elements for data to be uploaded as files
#     Return (content_type, body) ready for httplib.HTTP instance
#     """
#     BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
#     CRLF = '\r\n'
#     L = []
#     for (key, value) in fields:
#         L.append('--' + BOUNDARY)
#         L.append('Content-Disposition: form-data; name="%s"' % key)
#         L.append('')
#         L.append(value)
#     L.append('--' + BOUNDARY + '--')
#     L.append('')
#     body = CRLF.join(L)
#     content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
#     return content_type, body
