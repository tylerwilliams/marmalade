import random
import config
config.TRACE_API_CALLS=True

import user

def random_walk(user, steps):
    followers = user.get_followers()
    for i in xrange(steps):
        new_user = random.choice(followers)
        print "%s follows %s" % (new_user, user)
        user = new_user
        followers = user.get_followers()
    
t = user.TIMJUser('tylerbw')
print t.get_followers(100)

# print t.get_bio()
# print t.get_url()
# print t.get_avatar('small')
# print t.get_avatar('normal')
# print '%i people that follow you:%s' % (t.get_num_followers(), ", ".join(f.id for f in t.get_followers()))
# print '%s people you follow:%s' % (t.get_num_followees(), ", ".join(f.id for f in t.get_followees()))
# print t.get_num_jams()
# print t.get_full_name()
# print t.get_joined_date()
# print t.get_representative_artists()
# print t