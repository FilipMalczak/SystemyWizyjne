package com.github.wizyjne

/**
 * For now works only when CWD is repository root.
 */
class Resources {
    static File getExample(String name){
        new File("../../../../../../klipy/${name}")
    }
}
