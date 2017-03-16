import argparse
from pyniland.client import Client
import sys

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

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
