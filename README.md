## Description

In the real-world, there are many ways to exploit via css injection. the way what I talk now which help to leak data without other vulnerabilities so we can leak data only via css-injection.

```
blob:https://example.com/f915e403-0d27-459d-8bc6-8a91ee491aaf
```
If there is a blob-url as above, do you have any idea to leak the uuid via css injection? maybe you guys try to leak it like brute-force as `blob:https://example.com/a`, `blob:https://example.com/b`, `blob:https://example.com/c` while chaning a character. well but you need to find next character even if you found the correct first character of the uuid like `blob:https://example.com/f`. however how can you make that css injection file recognizes the correct character of the uuid what you found before. 

```
blob:https://example.com/f
blob:https://example.com/f9
blob:https://example.com/f91
~
blob:https://example.com/f915e403-0d27-459d-8bc6-8a91ee491aaf
```
As you know well, css injection file must have the correct character of the uuid what you found before for doing step-to-step but it's impossible to make it with only css-injection cause your private server will get the data if exploit-code finds the correct character of the uuid. you need to xss if you want to interact with exploit-code and your private server so there is one way to leak the uuid.

```
f915e403-0d27-459d-8bc6-8a91ee491aaf

f91 => 915 => 15e => 5e4
```
you have to leak the number of all cases of the uuid which split to 3 characters then must find the last two characters of the first data and  the first two characters of the second data which are matching and link it. finally If you've already leaked the number of all cases of the uuid, try generating all uuids after giving the number of all cases a chance to be first.
