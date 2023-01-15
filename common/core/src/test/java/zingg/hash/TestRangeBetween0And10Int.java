package zingg.hash;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class TestRangeBetween0And10Int {

    private RangeInt getInstance() {
        return new RangeInt(0,10);
    }

	@Test
	public void testRangeForValueZero() {
	    RangeInt value = getInstance();
		assertEquals(1, value.call(0));
	}

	@Test
	public void testRangeForNegativeValue() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(-100));
	}

	@Test
	public void testRangeForVeryHighValue() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(999999));
	}

	@Test
	public void testRangeForValue8() {
	    RangeInt value = getInstance();
		assertEquals(1, value.call(8));
	}

	@Test
	public void testRangeForValue65() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(65));
	}

	@Test
	public void testRangeForValue867() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(867));
	}
	@Test
	public void testRangeForValue8637() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(8637));
	}
	@Test
	public void testRangeForNull() {
	    RangeInt value = getInstance();
		assertEquals(0, value.call(null));
	}

}