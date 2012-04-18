# Marmalade - A Python Client for [This Is My Jam](http://thisismyjam.com/)

 * Tastes Great
 * Good on Toast
 * Easy to use!

## INSTALL
    $ easy_install -U marmalade

## GETTING STARTED

    import marmalade

    me = marmalade.TIMJUser('tylerbw')
    def print_friends(user):
        print "Followers:"
        for i, follower in enumerate(user.get_followers(sort='affinity')):
            print '\t',i,':',follower.get_full_name()

    print_friends(me)

    def find_slacker_friends(user):
        return [friend for friend in user.get_followers() if not friend.has_current_jam()]

    print find_slacker_friends(me)

    a_jam = marmalade.Jam.from_user('flaneur')
    print a_jam.get_num_plays()

    def find_most_popular_follower(user):
        return sorted((friend.get_num_followers(),friend) for friend in user.get_followers())[-1][1]

    print find_most_popular_follower(me)

    import random
    def random_walk_generator(user, steps_away):
        yield user
        followers = user.get_followers()
        for _ in xrange(steps_away):
            new_user = random.choice(followers)
            yield new_user
            user = new_user
            followers = user.get_followers()

    print " ==> ".join(u.id for u in random_walk_generator(me, 4))
	
### ADVANCED
Look at the source or [test.py](https://github.com/tylerwilliams/marmalade/blob/master/test.py) for more examples.

## YUM
![alt text](https://raw.github.com/tylerwilliams/marmalade/master/marmalade.jpg "mmmmm (from: http://www.flickr.com/photos/wendycopley/4451578552/sizes/n/in/photostream/)")

    