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
