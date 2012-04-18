#!/usr/bin/env python
# encoding: utf-8

import datetime
import proxies
import util

def get_suggested_users(results=10):
    get_function = proxies.get_json_resource
    raw = proxies.get_listed_things(get_function, "suggestedPeople", 'people', results)
    return [TIMJUser(**util.fix(raw_person)) for raw_person in raw]

def _search_users_by(by, q, results):
    get_function = proxies.get_json_resource
    raw = proxies.get_listed_things(get_function, "search/person", 'people', results, by=by, q=q)
    return [TIMJUser(**util.fix(raw_person)) for raw_person in raw]

def search_users_by_artist(artist_q, results=10):
    return _search_users_by('artist', artist_q, results)

def search_users_by_name(user_name, results=10):
    return _search_users_by('name', user_name, results)

def search_users_by_track(artist_name, track_name, results=10):
    combined = "%s|%s" % (artist_name, track_name)
    return _search_users_by('track', combined, results)

class Jam(proxies.JamProxy):
    def __init__(self, id, **kwargs):
        super(Jam, self).__init__(id, **kwargs)

    """
        Jam
    """
    @classmethod
    def from_user(cls, username):
        raw_jam = proxies.get_json_resource(username).get('jam')
        if raw_jam:
            return cls(**util.fix(raw_jam))
        else:
            return None

    def get_artist(self):
        return self._get_simple_attribute('artist')
    
    def get_title(self):
        return self._get_simple_attribute('title')
    
    def get_caption(self):
        return self._get_simple_attribute('caption')
    
    def get_creation_date(self):
        creation_date = self._get_simple_attribute('creationDate')
        return datetime.datetime.strptime(creation_date, "%a, %d %b %Y %H:%M:%S +0000")

    def get_expiration_date(self):
        end_date = self._get_simple_attribute('endDate')
        return datetime.datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S +0000")

    def is_current_jam_for_user(self):
        return bool(self._get_simple_attribute('current'))
    
    def get_user(self):
        return TIMJUser(self._get_simple_attribute('from'))
    
    def get_num_likes(self):
        return self._get_simple_attribute('likesCount')
    
    def get_likes(self, results=10):
        users_who_liked = self._get_listed_things('likes', 'people', results)
        return [TIMJUser(**util.fix(raw_person)) for raw_person in users_who_liked]
    
    def get_jamvatar(self, size='large'):
        size = size.lower()
        assert size in ('small', 'medium', 'large')
        if size == 'small':
            key = 'jamvatarSmall'
        elif size == 'medium':
            key = 'jamvatarMedium'
        elif size == 'large':
            key = 'jamvatarLarge'
        return self._get_simple_attribute(key)
    
    def get_num_plays(self):
        return self._get_simple_attribute('playCount')
    
    def get_source(self):
        return self._get_simple_attribute('via')
    
    def get_url(self):
        return self._get_simple_attribute('viaUrl')
    
    def __repr__(self):
        return "Jam <%s>" % self.id

class TIMJUser(proxies.UserProxy):
    def __init__(self, name, **kwargs):
        super(TIMJUser, self).__init__(name, **kwargs)

    """
        This Is My Jam User
    """

    def get_bio(self):
        return self._get_simple_attribute('bio')

    def get_url(self):
        return self._get_simple_attribute('apiUrl')

    def get_avatar(self, size='normal'):
        size = size.lower()
        assert size in ('small', 'normal')
        if size == 'normal':
            key = 'avatarNormal'
        elif size == 'small':
            key = 'avatarSmall'
        return self._get_simple_attribute(key)
            
    def _get_friends_and_idols(self, person_type, results, sort=None):
        assert person_type in ('followers', 'following')
        paramd = {}
        if sort:
            assert sort in ('when', 'affinity', 'alpha')
            paramd['order'] = sort
        friends_and_idols = self._get_listed_things(person_type, 'people', results, **paramd)
        return [TIMJUser(**util.fix(raw_person)) for raw_person in friends_and_idols]

    def get_num_followers(self):
        return self._get_simple_attribute('followersCount')

    def get_followers(self, results=10, sort=None):
        return self._get_friends_and_idols('followers', results, sort=sort)

    def get_num_followees(self):
        return self._get_simple_attribute('followingCount')

    def get_followees(self, results=10, sort=None):
        return self._get_friends_and_idols('following', results, sort=sort)

    def get_full_name(self):
        return self._get_simple_attribute('fullname')
    
    def get_twitter_name(self):
        return self._get_simple_attribute('twitterName')
            
    def get_lastfm_name(self):
        return self._get_simple_attribute('lastfmName')
            
    def get_facebook_id(self):
        return self._get_simple_attribute('facebookID')
            
    def get_num_jams(self):
        return self._get_simple_attribute('jamCount')
    
    def get_joined_date(self):
        joined_on = self._get_simple_attribute('joinedDate')
        return datetime.datetime.strptime(joined_on, "%a, %d %b %Y %H:%M:%S +0000")
    
    def get_representative_artists(self):
        return self._get_simple_attribute('representativeArtists')
    
    def get_current_jam(self):
        jam = self.get_json_resource(self.id).get('jam')
        if jam:
            return Jam(**util.fix(jam))
        else:
            return None
    
    def has_current_jam(self):
        return bool(self._get_simple_attribute('hasCurrentJam'))
    
    def get_jams(self, results=10):
        raw_jams = self._get_listed_things('jams', 'jams', results)
        return [Jam(**util.fix(raw_jam)) for raw_jam in raw_jams]
    
    def get_liked_jams(self, results=10):
        liked_jams = self._get_listed_things('likes', 'jams', results)
        return [Jam(**util.fix(raw_jam)) for raw_jam in liked_jams]        
    
    def __repr__(self):
        return "TIMJUser <%s>" % self.id