import datetime
import proxies

# class Jam(proxies.JamProxy):
#     pass

class TIMJUser(proxies.UserProxy):
    def __init__(self, name, **kwargs):
        super(TIMJUser, self).__init__(name, **kwargs)

    """
        Yay docs.
    """
    def _get_simple_attribute(self, attribute_name):
        if not attribute_name in self.cache:
            profile = self.get_json_resource(self.id)['person']
            self.cache.update(profile)
        return self.cache.get(attribute_name)

    def get_bio(self):
        return self._get_simple_attribute('bio')

    def get_url(self):
        return self._get_simple_attribute('apiUrl')

    def get_avatar(self, size='normal'):
        if size == 'normal':
            return self._get_simple_attribute('avatarNormal')
        elif size == 'small':
            return self._get_simple_attribute('avatarSmall')

    def _get_friends_and_idols(self, person_type, results):
        assert person_type in ('followers', 'following')
        if results == -1:
            # hopefully you don't have more followers than this....
            # i'm looking at you wil wheaton
            results = int(1e4)
        friends_and_idols = []
        num_pages = max(results/10, 1)
        for page_num in xrange(num_pages):
            raw = self.get_json_user_attribute(person_type, page=page_num+1)
            people = raw['people']
            if not people:
                break
            friends_and_idols += people
        return [TIMJUser(**raw_person) for raw_person in friends_and_idols[:results]]

    def get_num_followers(self):
        return self._get_simple_attribute('followersCount')

    def get_followers(self, results=10):
        return self._get_friends_and_idols('followers', results)

    def get_num_followees(self):
        return self._get_simple_attribute('followingCount')

    def get_followees(self, results=10):
        return self._get_friends_and_idols('following', results)

    def get_full_name(self):
        return self._get_simple_attribute('fullname')
    
    def get_num_jams(self):
        return self._get_simple_attribute('jamCount')
    
    def get_joined_date(self):
        joined_on = self._get_simple_attribute('joinedDate')
        return datetime.datetime.strptime(joined_on, "%a, %d %b %Y %H:%M:%S +0000")
    
    def get_representative_artists(self):
        return self._get_simple_attribute('representativeArtists')
    
    def get_jam(self):
        raise NotImplementedError("tyler is lazy")
    
    def __repr__(self):
        return "TIMJUser <%s>" % self.id