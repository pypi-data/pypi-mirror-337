from simple_blogger import SimpleBlogger

class SimplestBlogger(SimpleBlogger):
    def _example_task_creator(self, _):
        return [ { "topic_prompt": "Topic prompt" } ]
    
    def _get_category_folder(self, _):
        return '.'
    
    def _task_post_processor(self, *_):
        pass

    def _task_converter(self, item):
        return item
    
    def _task_extractor(self, tasks, **_):
        return tasks[0]
    
    def review(self, type='topic', **kwargs):
        return super().review(type, force_image_regen=True, force_text_regen=True, **kwargs)

    def send(self, type='topic', image_gen=True, text_gen=True, days_offset=None, force_text_regen=True, force_image_regen=True, **kwargs):
        return super().send(type, image_gen, text_gen, days_offset=days_offset, force_text_regen=force_text_regen, force_image_regen=force_image_regen, **kwargs)
    
    def revert(self):
        pass