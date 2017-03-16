import argparse
# import requests
from pyniland.client import Client
import sys

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# def process(page, page_size, niland_url, niland_key, soundcloud_key,
#             delete_missing):
#     s = requests.Session()
#     a = requests.adapters.HTTPAdapter(max_retries=3)
#     b = requests.adapters.HTTPAdapter(max_retries=3)
#     s.mount('http://', a)
#     s.mount('https://', b)
#
#     url = '%s/tracks?page_size=%d&page=%d&key=%s' % (niland_url, page_size, page, niland_key)
#     general_niland_r = s.get(url).json()
#     ids = [tr['reference'] for tr in general_niland_r['data']]
#     url = 'https://api.soundcloud.com/tracks?ids=%s&client_id=%s' % (
#         ','.join([str(id) for id in ids]), soundcloud_key
#     )
#     general_soundcloud_r = s.get(url).json()
#
#     for track in general_soundcloud_r:
#         if not isinstance(track, dict):
#             break
#         url = '%s/tracks/reference/%d?key=%s' % (niland_url, track['id'], niland_key)
#         status = 0
#         while status != 200 and status != 404 and status != 500:
#             try:
#                 response = s.patch(
#                     url, {"popularity": track.get("playback_count", 0)}
#                 )
#                 status = response.status_code
#             except requests.ConnectionError:
#                 pass
#     if len(general_soundcloud_r) < len(ids) and delete_missing:
#         print "Missing %d tracks" % (len(ids) - len(general_soundcloud_r))
#         if len(ids) - len(general_soundcloud_r) > page_size / 5:
#             print "To many tracks to delete, might be a SCL error"
#         else:
#             print [id for id in ids if int(id) not in [tr['id'] for tr in general_soundcloud_r]]
#             for id in ids:
#                 if int(id) not in [tr['id'] for tr in general_soundcloud_r]:
#                     url = '%s/tracks/reference/%s?key=%s' % (
#                         niland_url, id, niland_key
#                     )
#                     print "deleting", url
#                     response = s.delete(url)

def are_you_sure():
    yes = set(['yes','y','ye'])

    print 'You are about to remove the tracks in your catalog. Are you sure you want to continue ? [y/N]'

    choice = raw_input().lower()

    if choice not in yes:
       return False

    print "\nThis action CANNOT be undone. This will permanently delete all tracks that have been uploaded to Niland's API."
    print "Please type in \"DELETE\" if you fully understand that this script is about to DELETE all your tracks :"

    choice = raw_input()
    if choice == 'DELETE':
        return True

    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', required=True)
    args = parser.parse_args()

    count = 0

    if not are_you_sure():
        print 'Exiting.'
    else:
        print "\nOk, your tracks are about to be deleted. This may take time, depending on the number of tracks that have been uploaded.\n"

        print 'Starting..'
        client = Client(args.api_key)
        page = 0

        while True:
            response = client.get('tracks', {'page': page, 'page_size': 1000})
            if len(response['data']) == 0:
                print '%d tracks have been successfully deleted.' % count
                print 'DONE'
                break

            tracks = response['data']

            for track in tracks:
                client.delete('tracks/%d' % track['id'])
                count += 1

                if count % 10000 == 0:
                    print '%d tracks deleted..' % count

            page += 1
