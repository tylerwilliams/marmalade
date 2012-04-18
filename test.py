import random
import pprint

import marmalade
from marmalade import config
config.TRACE_API_CALLS=True

t = marmalade.TIMJUser('tylerbw')

print t.get_twitter_name()
print t.get_lastfm_name()
print t.get_facebook_id()

pprint.pprint(t.get_followees(results=-1, sort='affinity'))
pprint.pprint(t.get_followers(results=-1, sort='affinity'))

print marmalade.get_suggested_users(1)
print marmalade.search_users_by_artist('beach boys', results=1)
print marmalade.search_users_by_name('andreas', results=-1)
print marmalade.search_users_by_track('lana del rey', 'video games')

def random_walk(user, steps):
    followers = user.get_followers()
    for _ in xrange(steps):
        new_user = random.choice(followers)
        print "%s follows %s" % (new_user, user)
        user = new_user
        followers = user.get_followers()

t = marmalade.TIMJUser('tylerbw')
print t
print t.get_bio()
print t.get_url()
print t.get_avatar('small')
print t.get_avatar('normal')
print '%i people that follow you:%s' % (t.get_num_followers(), ", ".join(f.id for f in t.get_followers()))
print '%s people you follow:%s' % (t.get_num_followees(), ", ".join(f.id for f in t.get_followees()))
print t.get_num_jams()
print t.get_full_name()
print t.get_joined_date()
print t.get_representative_artists()

print t.get_jams()
print t.get_current_jam()
print t.get_liked_jams()

j = marmalade.Jam('wuqexy')
print j
print j.get_likes(-1)
print j.get_artist()
print j.get_title()
print j.get_caption()
print j.get_creation_date()
print j.is_current_jam_for_user()
print j.get_user()
print j.get_jamvatar('small')
print j.get_jamvatar('medium')
print j.get_jamvatar('large')

j = marmalade.Jam.from_user('tylerbw')
print j
print j.get_likes(-1)
print j.get_artist()
print j.get_title()
print j.get_caption()
print j.get_creation_date()
print j.is_current_jam_for_user()
print j.get_user()
print j.get_jamvatar('small')
print j.get_jamvatar('medium')
print j.get_jamvatar('large')
print j.get_expiration_date()

print "here is what your followers are liking:"
most_popular_jam = None
for follower in t.get_followers(-1):
    j = follower.get_current_jam()
    if j:
        jamtext = "%s (%s - %s)" % (j, j.get_artist(), j.get_title())
        if not most_popular_jam or (j.get_num_likes() > most_popular_jam.get_num_likes()):
            most_popular_jam = j
    else:
        jamtext = "nothing!"
    print "%s ====> %s" % (follower, jamtext)

print "most liked jam was: %s, jammed by %s on %s (%s)\n" % (most_popular_jam,
                                                            most_popular_jam.get_user(),
                                                            most_popular_jam.get_creation_date(),
                                                            most_popular_jam.get_url())
random_walk(t,5)
