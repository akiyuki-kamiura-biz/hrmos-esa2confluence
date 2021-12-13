import os
import json


class EsaPost:
    def __init__(self, post_json):
        self.post_json = post_json

        self.number = post_json['number']
        self.name = post_json['name']
        self.full_name = post_json['full_name']
        self.wip = post_json['wip']
        self.body_md = post_json['body_md']
        self.body_html = post_json['body_html']
        self.created_at = post_json['created_at']
        self.message = post_json['message']
        self.url = post_json['url']
        self.updated_at = post_json['updated_at']
        self.tags = post_json['tags']
        self.category = post_json['category']
        self.revision_number = post_json['revision_number']
        self.created_by_name = post_json['created_by']['name']
        self.created_by_screen_name = post_json['created_by']['screen_name']
        self.updated_by_name = post_json['updated_by']['name']
        self.updated_by_screen_name = post_json['updated_by']['screen_name']
        self.comments = post_json['comments']

    def save_json(self, directory_path):
        dirs = self.full_name.split("/")[:-1]

        # make directories
        for i in range(len(dirs)):
            path = "/".join([directory_path] + dirs[:i+1])

            if not os.path.exists(path):
                os.makedirs(path)

        # save file
        file_path = "/".join([directory_path] + dirs + [self.name]) + ".json"
        output_file = open(file_path, 'w')
        json.dump(self.post_json, output_file)
        output_file.close()