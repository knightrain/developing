#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import inspect
import pygame
import wave

class Speaker():
    max_word_lookahead = 0
    mappings={}
    filedir = ""
    def __init__(self):
        this_file = inspect.getfile(inspect.currentframe())
        self.filedir = os.path.abspath(os.path.dirname(this_file))
        self.read_mandrin_list()

    def check_special_phon(self, zh_word, pinyin):
        zh_word = unicode(zh_word, "utf-8")
        pinyins = pinyin.split(' ')
        if zh_word[0] == unichr(0x4e00) or zh_word[0] == unichr(0x4e0d):
            if pinyins[0][-1] == "2":
                return False
        for i in range(len(zh_word)):
            if zh_word[i] == unichr(0x4e00) or zh_word[i] == unichr(0x4e0d):
                if i + 1 != len(zh_word) and pinyins[i][-1] == "2" and pinyins[i+1][-1] == "4":
                    pass
            if self.mappings.has_key(zh_word[i]):
                pin = self.mappings[zh_word[i]]
                pin = pin.split(' ')[0]
                if pin[-1] != pinyins[i][-1]:
                    return True 
            else:
                return True
        return False

    def read_mandrin_list(self):
        filename = os.path.join(self.filedir, "Mandarin.list")
        try:
            ifile = open(filename)
        except:
            print("**WARNING** Cannot open \""+filename+"\".")
            return()

        print "Loading " + filename + "..."
        self.max_word_lookahead = 0
        for l in ifile.xreadlines():
            zh_word, pinyin = l.strip().split(' ', 1)
            if '(' in zh_word:
                zh_word = zh_word.replace("(","").replace(")","").replace(" ","")
                for i in range(0, 10):
                    pinyin = pinyin.replace(str(i), str(i) + " ")
                pinyin.rstrip()
                if not self.check_special_phon(zh_word, pinyin):
                    continue
            zh_word = unicode(zh_word, "utf-8")
            self.mappings[zh_word] = pinyin
            self.max_word_lookahead = max(self.max_word_lookahead, len(zh_word))
        print "Loaded " + filename
        ifile.close()

    def print_list(self):
        for k, v in self.mappings.items():
            print "%s\t%s" % (k.encode("utf-8"), v)

    def handle_delayed(self, delayed, tone4):
        pinyins = self.mappings[delayed].split(" ")
        if tone4:
            pinyin = pinyins[0][:-1]+'2'
        else:
            pinyin = pinyins[0]
        return pinyin

    def words2pinyin(self, words):
        # convert to Unicode if not already
        if not type(words)==type(u""):
            words = unicode(words, "utf-8")
        pinyin_list = []
        i = 0
        length = len(words)
        delayed = None
        while i < len(words):
            found = False
            max_word_len = min(length-i, self.max_word_lookahead)
            for num_word in range(max_word_len, 0, -1):
                if words[i:i+num_word] in self.mappings:
                    pinyin = self.mappings[words[i:i+num_word]]
                    pinyins = pinyin.split(" ")
                    if num_word == 1 and len(pinyins) > 1:
                        if delayed != None:
                            print "after", pinyins[0]
                            pinyin_list.append(self.handle_delayed(delayed,
                                    words[i] != delayed and pinyins[0][-1] == '4'))
                            delayed = None
                        #delayed handling of "不" and "一"
                        if words[i] == unichr(0x4e00) or words[i] == unichr(0x4e0d):
                            delayed = words[i]
                        else: 
                            pinyin_list.append(pinyins[0])
                    else:
                        if delayed != None:
                            pinyin_list.append(self.handle_delayed(delayed,
                                    words[i] != delayed and pinyins[0][-1] == '4'))
                            delayed = None
                        for p in pinyins: pinyin_list.append(p);
                    found = True
                    i += num_word
                    break
            if not found:
                if delayed != None:
                    pinyin_list.append(self.handle_delayed(delayed, False))
                    delayed = None
                #TODO: handle punctuation
                pinyin_list.append('.')
                i += 1
        if delayed != None:
            pinyin_list.append(self.handle_delayed(delayed, False))
            delayed = None

        # handle tone 3
        # rules: 333->223, 33->23, 3333->2323
        def handle_tone3(tone3_list):
            ret = []
            while tone3_list:
                if len(tone3_list) == 3:
                    p = tone3_list.pop()
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop()
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop()
                    ret.append(p)
                elif len(tone3_list) >= 2:
                    p = tone3_list.pop()
                    p = p.replace('3', '2')
                    ret.append(p)
                    p = tone3_list.pop()
                    ret.append(p)
                else:
                    p = tone3_list.pop()
                    ret.append(p)
            return ret

        ret = []
        tone3 = []
        while pinyin_list:
            pinyin = pinyin_list.pop()
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
                data = data + '\0'*10000
            else:
                rf = wave.open(os.path.join(self.filedir, "voices\\pinyin", pinyin+".wav"), 'rb') 
                data = data + rf.readframes(rf.getnframes())
                data += '\0'*10000
                rf.close()
        sound = mixer.Sound(data)
        return sound.play()

def main():
    pygame.mixer.init(44100, -16, 1, 4096)
    speaker = Speaker()
    channel = speaker.speak_words(pygame.mixer, u"想想想想想")
    while channel.get_busy():
        pygame.time.wait(1000)

if __name__ == '__main__':
    main()
