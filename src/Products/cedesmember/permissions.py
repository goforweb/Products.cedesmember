# -*- coding: UTF-8 -*-
# Copyright (c) 2007 Webin Concept (Brussels, BELGIUM).
# http://www.webinconcept.be -- webinconcept@gmail.com

from Products.Archetypes import public as atapi
from Products.CMFCore import permissions as cmfcore_permissions

from Products.cedesmember import config
from Products.cedesmember.content.cedesmember import CedesMember

#Defines the permissions of CedesMEmber Content Types
 
# Add a new member
ADD_PERMISSION = ADD_MEMBER_PERMISSION = cmfcore_permissions.AddPortalMember

# The code below will create a unique add permission for each of your
# content types.  The permission for adding the type MyContentType will
# be 'MyProject: Add MyContentType'.  If instead you want to specify
# your own add permission (e.g. use the CMF's 'Add portal content'
# permission), you can use the ADD_PERMISSIONS dictionary to do so.

# ADD_PERMISSIONS is used to specify the name of the permission
# used for adding one of your content types.  For example:
#
# ADD_PERMISSIONS = {'MyFirstContentType': 'Add portal content',
#                    'MySecondContentType': 'My other permission',
#                   }

ADD_PERMISSIONS = {
                   CedesMember.portal_type: ADD_MEMBER_PERMISSION,
                   }
def initialize():
    permissions = {}
    types = atapi.listTypes(config.PROJECTNAME)
    for atype in types:
        portal_type = atype['portal_type']
        permission = ADD_PERMISSIONS.get(portal_type, None)
        if permission is None:
            # construct a permission on the fly
            permission = "%s: Add %s" % (config.PROJECTNAME,
                                         portal_type)
            cmfcore_permissions.setDefaultRoles(permission, ('Manager',))
        permissions[portal_type] = permission

    return permissions
