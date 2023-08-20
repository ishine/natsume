/* ----------------------------------------------------------------- */
/*           The Japanese TTS System "Open JTalk"                    */
/*           developed by HTS Working Group                          */
/*           http://open-jtalk.sourceforge.net/                      */
/* ----------------------------------------------------------------- */
/*                                                                   */
/*  Copyright (c) 2008-2016  Nagoya Institute of Technology          */
/*                           Department of Computer Science          */
/*                                                                   */
/* All rights reserved.                                              */
/*                                                                   */
/* Redistribution and use in source and binary forms, with or        */
/* without modification, are permitted provided that the following   */
/* conditions are met:                                               */
/*                                                                   */
/* - Redistributions of source code must retain the above copyright  */
/*   notice, this list of conditions and the following disclaimer.   */
/* - Redistributions in binary form must reproduce the above         */
/*   copyright notice, this list of conditions and the following     */
/*   disclaimer in the documentation and/or other materials provided */
/*   with the distribution.                                          */
/* - Neither the name of the HTS working group nor the names of its  */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission.   */
/*                                                                   */
/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND            */
/* CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,       */
/* INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF          */
/* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          */
/* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS */
/* BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          */
/* EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   */
/* TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     */
/* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON */
/* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   */
/* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY    */
/* OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           */
/* POSSIBILITY OF SUCH DAMAGE.                                       */
/* ----------------------------------------------------------------- */

#ifndef NJD_SET_ACCENT_PHRASE_RULE_H
#define NJD_SET_ACCENT_PHRASE_RULE_H

#ifdef __cplusplus
#define NJD_SET_ACCENT_PHRASE_RULE_H_START extern "C" {
#define NJD_SET_ACCENT_PHRASE_RULE_H_END   }
#else
#define NJD_SET_ACCENT_PHRASE_RULE_H_START
#define NJD_SET_ACCENT_PHRASE_RULE_H_END
#endif                          /* __CPLUSPLUS */

NJD_SET_ACCENT_PHRASE_RULE_H_START;

/* 
Rules that chain single words into accent phrases 
General rules are appplied before specific ones. 
*/

/* Level 1 (the most general)
1-1  デフォルトは別のアクセント句に
1-2  「名詞」の連続はくっつける
1-3  「形容詞」の後に「名詞」がきたら別のアクセント句に
1-4  「名詞,形容動詞語幹」の後に「名詞」がきたら別のアクセント句に
1-5  「動詞」の後に「形容詞」or「名詞」がきたら別のアクセント句に
1-6  「副詞」，「接続詞」，「連体詞」は単独のアクセント句に
1-7  「名詞,副詞可能」（すべて，など）は単独のアクセント句に
1-8  「助詞」or「助動詞」（付属語）は前にくっつける
1-9  「助詞」or「助動詞」（付属語）の後の「助詞」，「助動詞」以外（自立語）は別のアクセント句に
1-10 「*,接尾」の後の「名詞」は別のアクセント句に
1-11 「形容詞,非自立」は「動詞,連用*」or「形容詞,連用*」に接続する場合に前にくっつける
1-12 「動詞,非自立」は「動詞,連用*」or「名詞,サ変接続」に接続する場合に前にくっつける
1-13 「名詞」の後に「動詞」or「形容詞」or「名詞,形容動詞語幹」がきたら別のアクセント句に
1-14 「記号」は単独のアクセント句に
1-15 「接頭詞」は単独のアクセント句に
1-16 「*,*,*,姓」の後の「名詞」は別のアクセント句に
1-17 「名詞」の後の「*,*,*,名」は別のアクセント句に
1-18 「*,接尾」は前にくっつける
*/

/* Level 2 
2-1  「名詞,非自立」は「動詞」or「形容詞」に接続する場合に前にくっつける
2-2  「名詞,非自立」の後の「名詞,自立」は別のアクセント句に
2-3  「フィラー」or「感動詞」の後の単語は別のアクセント句に
2-4  「名詞」の後の「名詞,代名詞」は別のアクセント句に、「代名詞」の後の「名詞」は別のアクセント句に
2-5  「名詞,サ変接続」or「名詞,形容動詞語幹」の後の「動詞,サ変＊」は前にくっつける
*/

/* surface */
#define NJD_SET_ACCENT_PHRASE_CHOUON "ー"

/* pos */
#define NJD_SET_ACCENT_PHRASE_MEISHI "名詞"
#define NJD_SET_ACCENT_PHRASE_KEIYOUSHI "形容詞"
#define NJD_SET_ACCENT_PHRASE_DOUSHI "動詞"
#define NJD_SET_ACCENT_PHRASE_FUKUSHI "副詞"
#define NJD_SET_ACCENT_PHRASE_SETSUZOKUSHI "接続詞"
#define NJD_SET_ACCENT_PHRASE_RENTAISHI "連体詞"
#define NJD_SET_ACCENT_PHRASE_JODOUSHI "助動詞"
#define NJD_SET_ACCENT_PHRASE_JOSHI "助詞"
#define NJD_SET_ACCENT_PHRASE_KIGOU "記号"
#define NJD_SET_ACCENT_PHRASE_SETTOUSHI "接頭詞"
#define NJD_SET_ACCENT_PHRASE_FILLER "フィラー"
#define NJD_SET_ACCENT_PHRASE_KANDOUSHI "感動詞"

/* pos group1 */
#define NJD_SET_ACCENT_PHRASE_IPPAN "一般"
#define NJD_SET_ACCENT_PHRASE_HIJIRITSU "非自立"
#define NJD_SET_ACCENT_PHRASE_SAHEN_SETSUZOKU "サ変接続"
#define NJD_SET_ACCENT_PHRASE_SETSUBI "接尾"
#define NJD_SET_ACCENT_PHRASE_SETSUZOKUJOSHI "接続助詞"
#define NJD_SET_ACCENT_PHRASE_SHUUJOSHI "終助詞"
#define NJD_SET_ACCENT_PHRASE_JOSHIRUISETSUZOKU "助詞類接続"
#define NJD_SET_ACCENT_PHRASE_DAIMEISHI "代名詞"
#define NJD_SET_ACCENT_PHRASE_RENTAIKA "連体化"
#define NJD_SET_ACCENT_PHRASE_FUKUJOSHI "副助詞"

/* pos group2 */
#define NJD_SET_ACCENT_PHRASE_KEIYOUDOUSHI_GOKAN "形容動詞語幹"
#define NJD_SET_ACCENT_PHRASE_FUKUSHI_KANOU "副詞可能"
#define NJD_SET_ACCENT_PHRASE_INYOU "引用"

/* pos group3 */
#define NJD_SET_ACCENT_PHRASE_SEI "姓"
#define NJD_SET_ACCENT_PHRASE_MEI "名"

/* ctype */
#define NJD_SET_ACCENT_PHRASE_SAHEN "サ変"

/* cform */
#define NJD_SET_ACCENT_PHRASE_RENYOU "連用"
#define NJD_SET_ACCENT_PHRASE_GARUSETSUZOKU "ガル接続"

/* orig */
#define NJD_SET_ACCENT_PHRASE_SURU "する"
#define NJD_SET_ACCENT_PHRASE_NARU "なる"
#define NJD_SET_ACCENT_PHRASE_YARU "やる"
#define NJD_SET_ACCENT_PHRASE_IU_1 "言う"
#define NJD_SET_ACCENT_PHRASE_IU_2 "いう"
#define NJD_SET_ACCENT_PHRASE_DOU "どう"
#define NJD_SET_ACCENT_PHRASE_KOU "こう"
#define NJD_SET_ACCENT_PHRASE_SOU "そう"
#define NJD_SET_ACCENT_PHRASE_SUGIRU "すぎる"
#define NJD_SET_ACCENT_PHRASE_TOUTEN "、"
#define NJD_SET_ACCENT_PHRASE_KUTEN "。"
#define NJD_SET_ACCENT_PHRASE_JA "じゃ"
#define NJD_SET_ACCENT_PHRASE_IKERU "いける"
#define NJD_SET_ACCENT_PHRASE_NAI "ない"

/* other */
#define NJD_SET_ACCENT_PHRASE_TE "て"
#define NJD_SET_ACCENT_PHRASE_DE "で"

NJD_SET_ACCENT_PHRASE_RULE_H_END;

#endif                          /* !NJD_SET_ACCENT_PHRASE_RULE_H */
