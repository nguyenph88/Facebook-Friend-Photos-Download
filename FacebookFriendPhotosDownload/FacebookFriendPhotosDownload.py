import os, shutil, requests, sys, string


class FFBD:
    def __init__(self, token):
        self.token = token
        self.download_folder = 'Download'
        self.session = requests.Session()
        # only continue when token is valid
        self.isTokenValid = True if self.check_token() else False
        self.requested_user = None
        self.requested_user_folder = None
        self.total_images = 0

    def download(self, user_id):
        self.user_id = user_id
        if self.isTokenValid:
            self.requested_user = self.check_user_info()
            self.requested_user_folder = self.requested_user['metadata']['type'] + ' ' + self.requested_user[
                'name'] + ' (' + self.requested_user['id'] + ')'
            self.total_images = 0       #reset count
            self.main()
        else:
            print('Your token is not valid. Please check and re-enter your token.')

    def check_token(self):
        token_request_url = 'https://graph.facebook.com/me?fields=id&access_token=' + self.token
        token_request_response = self.session.get(token_request_url).json()
        if 'id' in token_request_response:
            print('Valid token! With token ID = ' + token_request_response['id'])
            return True
        else:
            print('Token is invalid or something went wrong!')
            sys.exit()

    def check_user_info(self):
        user_info_url = 'https://graph.facebook.com?access_token={token}&id={user_id}&fields=name,picture.url,metadata.type&metadata=1' \
            .format(token=self.token, user_id=self.user_id)
        user_info_response = self.session.get(user_info_url).json()
        if 'id' not in user_info_response:
            print('User is not valid, please recheck the id')
            sys.exit()
        return user_info_response

    def remove_user_id_folder_if_exists_and_create_new_one(self):
        current_dir = os.getcwd()
        # check /Download path
        download_path = os.path.join(current_dir, self.download_folder)
        download_path_exists = os.path.isdir(download_path)
        if not download_path_exists:
            os.mkdir(download_path)
        # check user's folder path
        user_folder_path = os.path.join(current_dir, self.download_folder, self.requested_user_folder)
        user_folder_exists = os.path.isdir(user_folder_path)
        if user_folder_exists:
            print('User folder exists. Removing it ...')
            shutil.rmtree(user_folder_path)
        print('Creating user folder ...')
        os.mkdir(user_folder_path)

    def create_album_name(self, name):
        current_dir = os.getcwd()
        album_name_path = os.path.join(current_dir, self.download_folder, self.requested_user_folder, name)
        os.mkdir(album_name_path)

    def download_image(self, album_name, img_name, img_url):
        current_dir = os.getcwd()
        img_path = os.path.join(current_dir, self.download_folder, self.requested_user_folder, album_name,
                                img_name) + '.jpg'
        f = open(img_path, 'wb')
        f.write(requests.get(img_url).content)
        f.close()
        self.total_images = self.total_images + 1

    def main(self):
        print('You are requesting to download photos from: ' + self.requested_user_folder)
        albums_link = 'https://graph.facebook.com/{user_id}/albums?fields=id,name&limit=100&access_token={token}' \
            .format(user_id=self.user_id, token=self.token)

        # Cleanup user folder if exists
        self.remove_user_id_folder_if_exists_and_create_new_one()

        # !IMPORTANT: assuming users have no more than 100 albums, if not, im fucked
        albums_response = self.session.get(albums_link).json()
        print('This user has ' + str(len(albums_response['data'])) + ' albums. Processing ...')

        already_created_album_list = []
        for album_dict in albums_response['data']:
            # strip out all illegal chars for file name
            invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.']
            album_name = ''.join(c for c in album_dict['name'] if c not in invalid_chars)
            # remove leading and trailing space
            album_name = album_name.strip()
            # check for duplicated album name, add count to the end
            if album_name not in already_created_album_list:
                already_created_album_list.append(album_name)
            else:
                album_name = album_name + ' ' + str(sum(album_name in s for s in already_created_album_list) + 1)
            self.create_album_name(album_name)
            # loop through every album and json responses
            album_link = 'https://graph.facebook.com/{album_id}/photos?fields=source&access_token={token}' \
                .format(album_id=album_dict['id'], token=self.token)
            album_response = self.session.get(album_link).json()

            while True:
                try:
                    for img_link_dict in album_response['data']:
                        img_url = img_link_dict['source']
                        img_name = img_link_dict['id']
                        print('\nDownloading Album: ' + album_name + ' / ' + img_name + '.jpg' + '\nURL: ' + img_url)
                        self.download_image(album_name, img_link_dict['id'], img_link_dict['source'])
                    album_response = self.session.get(album_response['paging']['next']).json();

                    ### IMPORTANT: LAST PAGE IS NOT BEING READED
                except KeyError:
                    # When there are no more pages (['paging']['next']), load the of response
                    # then break from the loop and end the script.
                    for img_link_dict in album_response['data']:
                        img_url = img_link_dict['source']
                        img_name = img_link_dict['id']
                        print('\nDownloading Album: ' + album_name + ' / ' + img_name + '.jpg' + '\nURL: ' + img_url)
                        self.download_image(album_name, img_link_dict['id'], img_link_dict['source'])
                    break

        print('===============================================')
        print('Images Downloaded: ' + str(self.total_images))
        # there is an additional feeds to download for other types / but never had this branch happened
        # if account_type != 'user' and account_type != 'page':
        #     return None
