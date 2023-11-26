"""
Public + Private key to be used when *faking* authentication locally.
Not for real usage in deployed versions.
"""
jwk_public = {
    "kty": "RSA",
    "e": "AQAB",
    "use": "sig",
    "kid": "OIJBUpHzcZ01M751y5rcBylezlaD9ec92ZFK9CecMzs",
    "alg": "RS256",
    "n": "q4lI9gAyV98RNrIBhUxqaCDFmuiGfyrNVTrJ_Zf445zDyy7H_YEev7mJJB_ZfmeO_S_N4LLlfXelZy_XLZVKXyh"
         "8Zo-aW7SqlddjmEDihhMxS1kSTz74AgmCetQ5IdXdYgMwr6lr3ED4OxU7TRkbend5xGEGYZMHAwxT9fa_9zkqny"
         "Sb0ePfreBzVt0nGE8AqHt4X1fx6hZZ2ZN6-YOJo1O7gRT4e6QFVQymuwQjHPSb67_ssvvzJVeNxRHBJFu_bie6K"
         "eWmoMwrw7xxt84f7JnP5M1hy910G07ui2tBO-16gv67FV3FfyQzzUYxUsBSN95LxpR2sR-_r9bM0irQ3Q"
}

key_pair = {
    "p": "1r79XY8rqVEPy7iLL-FSybcx0mdAyXeiGLSZ9-fFTQrqrL8pBNfJbWXigssnoe19doHzS12USbBi8VgauUfe1Cj"
         "N-qcu91zuE4QMzjCZx42VxD4r8Bm4RKdIUoi_6vWC3ypYR2SpOlBWgZQc8a2AWbL_FZacaR2z9DXP8O0o7C8",
    "kty": "RSA",
    "q": "zH1HStG_Xs8i8QA4PnQ6VnKpCMvEPgjkjQ3Xb-cQjZZDTTP_xns7Pema4hynRx6U9IfOlY-y7mxrf7bv_a3IkWp"
         "UbxcWoc24uJJVP39dTHgLK8LAhk_eUsN6mq3JIlMzenHKRFr2lgBgFdDD04Gn8DaJvPAWcQYDEAkDii0GFLM",
    "d": "JkbcIQiqMzFzheDytev3UoT9kzOPz5CdgQc9S3k98IxqpEwsFEVbtyyPjaANyEcTgSvJpPpGe1jXb88dFO7bSaC"
         "fIcOpjg0ig40sjCzuXzypI0cc7tH-RXYZx47TsNkoLVbI5mnHx743pfd25B1WJF3Eri14Xw2P4v49PgVxkJizfT"
         "y79dmRP-wjc-QJdmwMzDTK3bki1atbZE4WOM_I3ZHPPvwUl5v3WoY9CgQ2kM3oWoV12wgZNC5kWbn4a7OS2Wy2J"
         "U3xswtj7irdZ2J1JXUjgJYP8D4fwMV9BpPzQ7JphRpc9aUNsO6EmEcJemfScqhgBgEyDdvw96bl9UgbgQ",
    "e": "AQAB",
    "use": "sig",
    "kid": "OIJBUpHzcZ01M751y5rcBylezlaD9ec92ZFK9CecMzs",
    "qi": "TXH4zN1Hp1Y3Ig4d05snOWDfbQ9S7ye3LXaYnoZRZcegn9icy7AfS73_CBXOMFVpTtWFbjATZgEnA51EuxG0heY"
          "bzn7GfCDTzPLeol5IiTCe5Gg2rNg0yWZ2l7SOo8Euqb0eKwB422WjOsTm6S4cjRh1JqdAoiFPjXTGlZTIfMA",
    "dp": "OftBb6R7dnDjoe7G7fuZncsv0Y59aKg7hQ4mUFAs7ntXF6NZkOwuf7I1sXjmz4rPCFNX_G5c3nSYkm9mb8Ze_Mu"
          "zqczAGpvl0DEkP_vRWZb57A2ZUW-wWCEOnvI7V1ZIqrbFNSmRo6QTZ1M1aW-eKxnwU8ThoGQbtYFeDsAJ_5M",
    "alg": "RS256",
    "dq": "jEG1X30kDIx4g-LJsRSZWugERrM0o_QHhzQiO2-6K9MP0GlFG0c06A9Nm59ZoO857cskh_LrIJue1BeO3mmPMyZ"
          "CSXwFmu92rqo37HiYbrW7u8U1tiob7JqFgoiGd5OnsGlR-baGgXY6cVwipPS-UoWlzcDDM7yS5zG3itO84v8",
    "n": "q4lI9gAyV98RNrIBhUxqaCDFmuiGfyrNVTrJ_Zf445zDyy7H_YEev7mJJB_ZfmeO_S_N4LLlfXelZy_XLZVKXyh8"
         "Zo-aW7SqlddjmEDihhMxS1kSTz74AgmCetQ5IdXdYgMwr6lr3ED4OxU7TRkbend5xGEGYZMHAwxT9fa_9zkqnySb"
         "0ePfreBzVt0nGE8AqHt4X1fx6hZZ2ZN6-YOJo1O7gRT4e6QFVQymuwQjHPSb67_ssvvzJVeNxRHBJFu_bie6KeWm"
         "oMwrw7xxt84f7JnP5M1hy910G07ui2tBO-16gv67FV3FfyQzzUYxUsBSN95LxpR2sR-_r9bM0irQ3Q"
}

local_jwks = {
    "keys": [
        jwk_public
    ]
}

