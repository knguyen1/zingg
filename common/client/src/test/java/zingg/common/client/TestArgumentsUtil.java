package zingg.common.client;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class TestArgumentsUtil {
    @Test
    void testFoo() throws Throwable {
        final ArgumentsUtil argsUtil = new ArgumentsUtil();
        final IArguments iArguments = argsUtil.createArgumentsFromJSON("s3a://mlp-ctbdt-adhoc-analytics-nonprd/zingg/amazon-google-config.json");

        assertTrue(true);
    }
}