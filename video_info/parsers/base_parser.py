# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 11:05
---------
@summary: 提供一些操作数据库公用的方法
---------
@author: Boris
'''
import sys
sys.path.append('../../')
import init

import utils.tools as tools
from db.elastic_search import ES
from emotion.emotion import Emotion
# from db.mongodb import MongoDB

es = ES()
emotion_obj = Emotion()
# mongodb = MongoDB()

def add_net_program(rank, rank_wave, url, name, video_id, image_url, mini_summary, episode_msg, today_play_count, total_play_count, director, classify, institution, release_year, description, actor, score, video_type, net_source):
    '''
    @summary:
    ---------
    @param rank:
    @param rank_wave:
    @param url:
    @param name:
    @param video_id:
    @param image_url:
    @param mini_summary:
    @param episode_msg:
    @param today_play_count:
    @param total_play_count:
    @param director:
    @param classify:
    @param institution:
    @param release_year:
    @param description:
    @param actor:
    @param score:
    @param type: 节目类型  电影 1 电视剧 2 综艺等
    @param net_source: 来源 爱奇艺
    ---------
    @result:
    '''

    program = {
        'rank' : rank,
        'rank_wave' : rank_wave,
        'url' : url,
        'program_name' : name,
        'image_url' : image_url,
        'keywords' : mini_summary,
        'episode' : episode_msg,
        'play_count_total' : today_play_count,
        'total_play_count' : total_play_count,
        'director' : director,
        'classify' : classify,
        'institution' : institution,
        'release_year' : release_year,
        'description' : description,
        'actor' : actor,
        'score' : score,
        'type':video_type,
        'net_source':net_source,
        'record_time': tools.get_current_date(),
        'is_setmenu':0,
        'baidu_score': None,
        'up_count' : None,
        'collect':0,
        'sensitive':0,
        'program_id':video_id
    }

    es.add('tab_mms_net_program', program, video_id)

def add_article(article_id, head_url, name, release_time, title, content, image_urls, watch_count, up_count, comment_count, program_id, gender, url = '', info_type = 3, emotion = 2, collect = 0, source = None):
    '''
    @summary:
    ---------
    @param article_id:
    @param head_url:
    @param name:
    @param release_time:
    @param title:
    @param content:
    @param image_urls:
    @param watch_count:
    @param up_count:
    @param comment_count:
    @param program_id:
    @param gender:
    @param url:
    @param info_type: 微信 、 微博、 视频等
    @param emotion:
    @param collect:
    @param source:
    ---------
    @result:
    '''

    emotion = emotion_obj.get_emotion((title or '') + content)
    article = {
        'article_id' : article_id,
        'program_id' : program_id,
        'release_time' : release_time,
        'content' : content,
        'head_url' : head_url,
        'consumer' : name,
        'comment_count' : comment_count,
        'info_type' : info_type,
        'up_count' : up_count,
        'title' : title,
        'emotion' : emotion,
        'image_url' : image_urls,
        'collect' : collect,
        'source' : source,
        'gender' : gender,
        'watch_count': watch_count,
        'url' : url,
        'record_time': tools.get_current_date()
    }

    if es.get('tab_mms_article', article_id):
        return False
    else:
        es.add('tab_mms_article', article, article_id)
        return True


def add_comment(comment_id, pre_id, article_id, consumer, head_url, gender, content, up_count, release_time, emotion, hot_id):

    emotion = emotion_obj.get_emotion(content)
    comment = {
        'id': comment_id,
        'article_id' : article_id,
        'pre_id' : pre_id,
        'release_time' : release_time,
        'content' : content,
        'head_url' : head_url,
        'consumer' : consumer,
        'up_count' : up_count,
        'emotion' : emotion,
        'hot_id' : hot_id,
        'gender' : gender,
        'record_time':tools.get_current_date()
    }

    if es.get('tab_mms_comments', comment_id):
        return False
    else:
        es.add('tab_mms_comments', comment, comment_id)
        return True

def add_weibo_user(program_id, user_id, name, url, image_url, verified_reason, is_verified, area, sex,
                   summary, fans_count, follow_count):
    weibo_user = {
        'program_id' : program_id,
        'user_id' : user_id,
        'name' : name,
        'url' : url,
        'image_url' : image_url,
        'verified_reason' : verified_reason,
        'is_verified' : is_verified,
        'area' : area,
        'sex' : sex,
        'summary' : summary,
        'fans_count' : fans_count,
        'follow_count' : follow_count
    }

    es.add('tab_mms_weibo_user', weibo_user, user_id)