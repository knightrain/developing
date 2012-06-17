#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
import pygame
import wave
import re

gloable_enc = 'gbk'
def decode_str(words):
    try:
        words = words.decode(gloable_enc)
        return words
    except:
        pass

    for c in ('utf-8', 'gbk', 'big5', 'jp', 'utf16','utf32'):
        try:
            words = words.decode(c)
            gloable_enc = c
            break
        except:
            pass
    return words 
    
class Speaker():
    max_word_lookahead = 0
    mappings={}
    def __init__(self):
        this_file = inspect.getfile(inspect.currentframe())
        self.filedir = os.path.abspath(os.path.dirname(this_file))
        self.check_resource()
        self.read_mandrin_list()
        self.add_special_symbol()
        self.regex_point = re.compile(r'(\d)\.(\d)')
        self.regex_sub = re.compile(u'[\.\?!。？！]')

    def check_resource(self):
        wave_file = os.path.join(self.filedir, "voices\\pinyin", "a1.wav")
        if os.path.isfile(wave_file):
            rf = wave.open(wave_file, 'rb')
            self.nchannels, self.sampwidth, self.framerate, \
            self.nframes, self.omptype, self.compname = rf.getparams()
            rf.close()

            # fullpause is 0.5 secs
            self.fullpause = '\0'*(self.framerate/2)*self.sampwidth
            self.halfpause = '\0'*(self.framerate/4)*self.sampwidth
            self.quaterpause = '\0'*(self.framerate/8)*self.sampwidth
        else:
            self.nchannels = 0
            self.sampwidth = 0
            self.framerate = 0
            self.nframes = 0
            self.omptype = 0
            self.compname = 0

    def read_mandrin_list(self):
        filename = os.path.join(self.filedir, "Mandarin.list")
        try:
            ifile = open(filename)
        except:
            print("**WARNING** Cannot open \""+filename+"\".")
            return

        print "Loading " + filename + "..."
        self.max_word_lookahead = 0
        for l in ifile:
            zh_word, pinyin = l.strip().split(' ', 1)
            if '(' in zh_word:
                zh_word = zh_word.replace("(","").replace(")","").replace(" ","")
            pinyins = pinyin.rstrip().split(' ')
            zh_word = unicode(zh_word, "utf-8")
            self.mappings[zh_word] = pinyins
            self.max_word_lookahead = max(self.max_word_lookahead, len(zh_word))
        print "Loaded " + filename
        ifile.close()

    def add_special_symbol(self):
        self.mappings[u'\n'] = '.'
        self.mappings[u';'] = '.'
        # Chinese ;
        self.mappings[unichr(0xff1b)] = '.'
        self.mappings[u'.'] = '.'
        # Chinese .
        self.mappings[unichr(0x3002)] = '.'
        self.mappings[u'!'] = '.'
        self.mappings[u'?'] = '.'
        self.mappings[u'...'] = '.'
        # Chinese ...
        self.mappings[unichr(0x2026)] = '.'

        self.mappings[u','] = ','
        self.mappings[unichr(0xff0c)] = ','
        self.mappings[u':'] = ','
        self.mappings[unichr(0xff1a)] = ','

        self.mappings[u'-'] = ' '
        # Chinese -
        self.mappings[unichr(0x2014)] = ' '
        self.mappings[u' '] = ' '
        # Chinese ' '
        self.mappings[unichr(0x3000)] = ' '
        self.mappings[u"'"] = ' '
        # ‘ 
        self.mappings[unichr(0x2018)] = ' '
        self.mappings[u'"'] = ' '
        # “ 
        self.mappings[unichr(0x201c)] = ' '
        self.mappings[u'('] = ' '
        # （
        self.mappings[unichr(0xff08)] = ' '
        self.mappings[u')'] = ' '
        # ） 
        self.mappings[unichr(0xff09)] = ' '
        # 《 
        self.mappings[unichr(0x300a)] = ' '
        # 》
        self.mappings[unichr(0x300b)] = ' '
        # 【
        self.mappings[unichr(0x300c)] = ' '
        # 】
        self.mappings[unichr(0x300d)] = ' '
        # Chinese "[["
        self.mappings[unichr(0x300e)] = ' '
        # Chinese "]]"
        self.mappings[unichr(0x300f)] = ' '

    def print_list(self):
        for k, v in self.mappings.items():
            print "%s\t%s" % (k.encode("utf-8"), v)

    def handle_delayed(self, delayed, tone4):
        pinyins = self.mappings[delayed]
        if tone4:
            pinyin = pinyins[0][:-1]+'2'
        else:
            pinyin = pinyins[0]
        return pinyin

    def words2pinyin(self, words):
        pinyin_list = []
        i = 0
        length = len(words)
        delayed = None
        while i < len(words):
            found = False
            max_word_len = min(length-i, self.max_word_lookahead)
            for num_word in range(max_word_len, 0, -1):
                if words[i:i+num_word] in self.mappings:
                    pinyins = self.mappings[words[i:i+num_word]]
                    if num_word == 1 and len(pinyins) > 1:
                        if delayed != None:
                            p = self.handle_delayed(delayed,
                                    words[i] != delayed and pinyins[0][-1] == '4')
                            pinyin_list.append(p)
                            delayed = None
                        #delayed handling of "不" and "一"
                        if words[i] == unichr(0x4e00) or words[i] == unichr(0x4e0d):
                            delayed = words[i]
                        else: 
                            pinyin_list.append(pinyins[0])
                    else:
                        if delayed != None:
                            p = self.handle_delayed(delayed,
                                    words[i] != delayed and pinyins[0][-1] == '4')
                            pinyin_list.append(p)
                            delayed = None
                        for p in pinyins: pinyin_list.append(p);
                    found = True
                    i += num_word
                    break
            if not found:
                if delayed != None:
                    p = self.handle_delayed(delayed, False)
                    pinyin_list.append(p)
                    delayed = None
                pinyin_list.append('.')
                i += 1
        if delayed != None:
            p = self.handle_delayed(delayed, False)
            pinyin_list.append(p)
            delayed = None

        # handle tone 3
        # rules: 333->223, 33->23, 3333->2323
        def handle_tone3(tone3_list):
            ret = []
            while tone3_list:
                if len(tone3_list) == 3:
                    p = tone3_list.pop(0)
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop(0)
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop(0)
                    ret.append(p)
                elif len(tone3_list) >= 2:
                    p = tone3_list.pop(0)
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop(0)
                    ret.append(p)
                else:
                    p = tone3_list.pop(0)
                    ret.append(p)
            return ret

        ret = []
        tone3 = []
        while pinyin_list:
            pinyin = pinyin_list.pop(0)
            if pinyin[-1] == '3':
                tone3.append(pinyin)
            else:
                if tone3:
                    ret = ret + handle_tone3(tone3)
                ret.append(pinyin)
        if tone3:
            ret = ret + handle_tone3(tone3)

        return ret

    def speak_words(self, mixer, words):
        pinyins = self.words2pinyin(words)
        data = ""
        for pinyin in pinyins:
            if pinyin == '.':
                data += self.fullpause
            elif pinyin == ',':
                data += self.halfpause
            elif pinyin == ' ':
                data += self.quaterpause
            else:
                wave_file = os.path.join(self.filedir, "voices\\pinyin", pinyin+".wav")
                if os.path.isfile(wave_file):
                    rf = wave.open(wave_file, 'rb') 
                    data += rf.readframes(rf.getnframes())
                    data += self.quaterpause
                    rf.close()
                else:
                    data += self.quaterpause
        nsamps = len(data) / self.sampwidth
        sound = mixer.Sound(data)
        return nsamps, sound.play()

    def preprocess_str(self, string):
        words = decode_str(string)
        return self.regex_point.sub(r'\1'+u'点'+r'\2', words);

def main():
    speaker = Speaker()
    pygame.mixer.init(speaker.framerate, speaker.sampwidth*8, speaker.nchannels, 4096)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as text:
            for l in text:
                l = speaker.preprocess_str(l)
                sentences = speaker.regex_sub.split(l)
                for s in sentences:
                    nsamps, channel = speaker.speak_words(pygame.mixer, s+'.')
                    sound_length = int(1000*nsamps/speaker.framerate)
                    pygame.time.wait(sound_length)
                    while channel.get_busy():
                        pygame.time.wait(100)
    else:
        text = speaker.preprocess_str(u"想想.普普想1.0想")
        nsamps, channel = speaker.speak_words(pygame.mixer, text)
        sound_length = 1000*nsamps/speaker.framerate
        pygame.time.wait(sound_length)
        while channel.get_busy():
            pygame.time.wait(100)

if __name__ == '__main__':
    main()
