" Vim color file
"
" Author: Peter Fern <github@0xc0dedbad.com>
"
" Note: Based on the Molokai theme for Vim
" by Tomas Restrepo, which is in turn based
" on the monokai theme for textmate by 
" Wimer Hazenberg and its darker variant 
" by Hamish Stuart Macpherson
"

hi clear

set background=dark
if version > 580
    " no guarantees for version 5.8 and below, but this makes it stop
    " complaining
    hi clear
    if exists("syntax_on")
        syntax reset
    endif
endif
let g:colors_name="molokai_pdf"

if exists("g:molokai_original")
    let s:molokai_original = g:molokai_original
else
    let s:molokai_original = 0
endif


hi Boolean         guifg=#875FAF
hi Character       guifg=#D7D787
hi Number          guifg=#875FAF
hi String          guifg=#D7D787
hi Conditional     guifg=#FF005F
hi Constant        guifg=#AF5FAF
hi Cursor          guifg=#000000 guibg=#F8F8F0
hi Debug           guifg=#BCA3A3               gui=bold
hi Define          guifg=#FF00AF
hi Delimiter       guifg=#8F8F8F
hi DiffAdd                       guibg=#13354A
hi DiffChange      guifg=#89807D guibg=#4C4745
hi DiffDelete      guifg=#960050 guibg=#1E0010
hi DiffText                      guibg=#4C4745 gui=italic,bold

hi Directory       guifg=#AFD700               gui=bold
hi Error           guifg=#960050 guibg=#1E0010
hi ErrorMsg        guifg=#FF005F guibg=#192729 gui=bold
hi Exception       guifg=#AFD700               gui=bold
hi Float           guifg=#875FAF
hi FoldColumn      guifg=#465457 guibg=#000000
hi Folded          guifg=#465457 guibg=#000000
hi Function        guifg=#AFD700
hi Identifier      guifg=#FD971F
hi Ignore          guifg=#808080 guibg=bg
hi IncSearch       guifg=#C4BE89 guibg=#000000

hi Keyword         guifg=#FF00AF
hi Label           guifg=#D7D787               gui=none
hi Macro           guifg=#C4BE89               gui=italic
hi SpecialKey      guifg=#66D9EF               gui=italic

hi MatchParen      guifg=#FF8700 guibg=#4E4E4E gui=bold
hi ModeMsg         guifg=#D7D787
hi MoreMsg         guifg=#D7D787
hi Operator        guifg=#FF005F

" complete menu
hi Pmenu           guifg=#AFD700 guibg=#121212
hi PmenuSel                      guibg=#808080
hi PmenuSbar                     guibg=#080808
hi PmenuThumb      guifg=#66D9EF

hi PreCondit       guifg=#AFD700               gui=bold
hi PreProc         guifg=#AFD700
hi Question        guifg=#66D9EF
hi Repeat          guifg=#FF005F
hi Search          guifg=#FFFFFF guibg=#455354
" marks column
hi SignColumn      guifg=#AFD700 guibg=#192729
hi SpecialChar     guifg=#FF005F
hi SpecialComment  guifg=#7E8E91               gui=bold
hi Special         guifg=#66D9EF guibg=bg      gui=italic
if has("spell")
    hi SpellBad    guisp=#FF0000 gui=undercurl
    hi SpellCap    guisp=#7070F0 gui=undercurl
    hi SpellLocal  guisp=#70F0F0 gui=undercurl
    hi SpellRare   guisp=#FFFFFF gui=undercurl
endif
hi Statement       guifg=#FF005F gui=none
hi StatusLine      guifg=#455354 guibg=fg
hi StatusLineNC    guifg=#808080 guibg=#080808
hi StorageClass    guifg=#FD971F               gui=italic
hi Structure       guifg=#66D9EF
hi Tag             guifg=#FF005F
hi Title           guifg=#ef5939
hi Todo            guifg=#FFFFFF guibg=bg      gui=bold

hi Typedef         guifg=#66D9EF
hi Type            guifg=#66D9EF               gui=none
hi Underlined      guifg=#808080               gui=underline

hi VertSplit       guifg=#808080 guibg=#080808 gui=bold
hi VisualNOS                     guibg=#403D3D
hi Visual                        guibg=#403D3D
hi WarningMsg      guifg=#FFFFFF guibg=#333333 gui=bold
hi WildMenu        guifg=#66D9EF guibg=#000000

hi Normal          guifg=#F8F8F2 guibg=#040404
hi Comment         guifg=#5f5f5f
hi CursorLine                    guibg=#121212
hi CursorLineNr    guifg=#D7FFAF
hi CursorColumn                  guibg=#121212
hi ColorColumn                   guibg=#121212
hi LineNr          guifg=#585858 guibg=#121212
hi NonText         guifg=#465457
hi SpecialKey      guifg=#465457

"
" Support for 256-color terminal
"
if &t_Co > 255
   hi Normal          ctermfg=252 ctermbg=16
   hi CursorLineNr    ctermfg=193
   hi CursorLine                  ctermbg=233   cterm=none
   hi Boolean         ctermfg=97
   hi Character       ctermfg=186
   hi Number          ctermfg=97
   hi String          ctermfg=186
   hi Conditional     ctermfg=197
   hi Constant        ctermfg=133
   hi Cursor          ctermfg=16  ctermbg=253
   hi Debug           ctermfg=225               cterm=bold
   hi Define          ctermfg=199
   hi Delimiter       ctermfg=241

   hi DiffAdd                     ctermbg=24
   hi DiffChange      ctermfg=181 ctermbg=239
   hi DiffDelete      ctermfg=162 ctermbg=53
   hi DiffText                    ctermbg=102 cterm=bold

   hi Directory       ctermfg=148               cterm=bold
   hi Error           ctermfg=219 ctermbg=89
   hi ErrorMsg        ctermfg=199 ctermbg=16    cterm=bold
   hi Exception       ctermfg=148               cterm=bold
   hi Float           ctermfg=97
   hi FoldColumn      ctermfg=67  ctermbg=16
   hi Folded          ctermfg=67  ctermbg=16
   hi Function        ctermfg=148
   hi Identifier      ctermfg=208               cterm=none
   hi Ignore          ctermfg=244 ctermbg=232
   hi IncSearch       ctermfg=193 ctermbg=16

   hi Keyword         ctermfg=199
   hi Label           ctermfg=229               cterm=none
   hi Macro           ctermfg=193
   hi SpecialKey      ctermfg=81

   hi MatchParen      ctermfg=208  ctermbg=239 cterm=bold
   hi ModeMsg         ctermfg=229
   hi MoreMsg         ctermfg=229
   hi Operator        ctermfg=197

   " complete menu
   hi Pmenu           ctermfg=148  ctermbg=233
   hi PmenuSel                    ctermbg=244
   hi PmenuSbar                   ctermbg=232
   hi PmenuThumb      ctermfg=81

   hi PreCondit       ctermfg=148               cterm=bold
   hi PreProc         ctermfg=148
   hi Question        ctermfg=81
   hi Repeat          ctermfg=197
   hi Search          ctermfg=253 ctermbg=66

   " marks column
   hi SignColumn      ctermfg=148 ctermbg=235
   hi SpecialChar     ctermfg=197
   hi SpecialComment  ctermfg=245               cterm=bold
   hi Special         ctermfg=81 

   hi Statement       ctermfg=197
   hi StatusLine      ctermfg=238 ctermbg=253
   hi StatusLineNC    ctermfg=244 ctermbg=232
   hi StorageClass    ctermfg=208
   hi Structure       ctermfg=81
   hi Tag             ctermfg=197
   hi Title           ctermfg=166
   hi Todo            ctermfg=231 ctermbg=232   cterm=bold

   hi Typedef         ctermfg=81
   hi Type            ctermfg=81                cterm=none
   hi Underlined      ctermfg=244               cterm=underline

   hi VertSplit       ctermfg=244 ctermbg=232   cterm=bold
   hi VisualNOS                   ctermbg=238
   hi Visual                      ctermbg=235
   hi WarningMsg      ctermfg=231 ctermbg=238   cterm=bold
   hi WildMenu        ctermfg=81  ctermbg=16

   hi Comment         ctermfg=59
   hi CursorColumn                ctermbg=233
   hi ColorColumn                 ctermbg=233
   hi LineNr          ctermfg=240 ctermbg=233
   hi NonText         ctermfg=59
   hi SpecialKey      ctermfg=59
end
