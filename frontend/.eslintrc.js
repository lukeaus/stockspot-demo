module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "ecmaFeatures": {
            "experimentalObjectRestSpread": true,
            "jsx": true
        },
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
    "rules": {
        "indent": [
            "error",
            2
        ],
        "no-console": 0,  // enable console.log statements
        "linebreak-style": [
            "error",
            "unix"
        ],
        "semi": [
            "error",
            "always"
        ]
    }
};
