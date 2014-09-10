from girder import events
from girder.utility.model_importer import ModelImporter


_groupName = 'Auto-join group'


def userSaved(event):
    """
    Adds any newly-created users the user to the auto-join group.
    """
    if '_id' in event.info:  # Only add to group at new user creation time.
        return

    groupModel = ModelImporter().model('group')
    cursor = groupModel.find({'name': _groupName}, limit=1, fields=('_id',))

    if cursor.count(True) > 0:
        group = cursor.next()
        event.info['groups'] = [group['_id']]


def load(info):
    events.bind('model.user.save', 'autojoin_group', userSaved)
