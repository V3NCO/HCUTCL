# HCUTCL

Everyone in the hackclub slack uses one thing : custom emojis. Kind of like a language that universal among hackclubbers. So i thought i would also make it into a programming language :)

## Plans

This started as just a brainfuck substitution (it still is for now), but it's gonna be more than that :
- [x] Uses a slack bot as it's interface
- [x] Uses Hackclub's emojis
- [x] Custom Interpreter in Python, Not from a translation to Brainfuck but directly in HCUTCL
- [ ] (Maybe) API for the compiler/interpreter ?
- [x] Custom `.` from brainfuck alternative
  - [x] Different Emojis for Variants : Output in ASCII, Hex? or Number
- [x] Input : use 2 Emojis to Open and close the input.
- [x] Help command that uses ***Block kit*** *(Block kit is required for #thunder)*

## Definitions

Emoji | Image of the Emoji | Purpose | Closest Brainfuck Equivalent
:-----|:------------------:|:--------|:----------------------------
:upvote:|<img src="https://emoji.slack-edge.com/T0266FRGM/upvote/7def7d0e61d71a56.png" width=32>|Increment the data pointer by one (to point to the next cell to the right).|`>`
:downvote:|<img src="https://emoji.slack-edge.com/T0266FRGM/downvote/9a040f9fd0d074af.png" width=32>|Decrement the data pointer by one (to point to the next cell to the left).|`<`
:yay:|<img src="https://emoji.slack-edge.com/T0266FRGM/yay/28592c2bf509c53f.gif" width=32>|Increment the byte at the data pointer by one.|`+`
:heavysob:|<img src="https://emoji.slack-edge.com/T0266FRGM/heavysob/55bf09f6c9d93d08.png" width=32>|Decrement the byte at the data pointer by one.|`-`
:pf:|<img src="https://emoji.slack-edge.com/T0266FRGM/pf/17de7f618b0ffa69.png" width=32>|Output the byte at the data pointer as an ASCII Character.|`.`
:sadge:|<img src="https://emoji.slack-edge.com/T0266FRGM/sadge/0964396d4a1f77f8.png" width=32>|Output the byte at the data pointer as a Number.|`.`
:3c:|<img src="https://emoji.slack-edge.com/T0266FRGM/3c/b853811bf0d800af.png" width=32>|Accept one byte of input, storing its value in the byte at the data pointer.|`,`
:dino-drake-yea:|<img src="https://emoji.slack-edge.com/T0266FRGM/dino-drake-yea/f30e5dfee629a60f.png" width=32>|If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching :dino-drake-nah: command.|`[`
:dino-drake-nah:|<img src="https://emoji.slack-edge.com/T0266FRGM/dino-drake-nah/ee4480a364d9ab18.png" width=32> |If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching :dino-drake-yea: command. |`]`
:uuh:|<img src="https://emoji.slack-edge.com/T0266FRGM/uuh/7ed2e8f6488ba1f3.png" width=32>|Open the input field which will be used to give data to `:3c:`.|
:noooovanish:|<img src="https://emoji.slack-edge.com/T0266FRGM/noooovanish/ebcb48d27469a989.png" width=32>|Close the input field which will be used to give data to `:3c:`.|

### Made for [Summer of Making](https://summer.hack.club/wg) and [Thunder YSWS](https://hackclub.slack.com/archives/C06V2GEV3MY) !!
