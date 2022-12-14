package zingg.spark.hash;

import org.apache.spark.sql.Column;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.functions;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.types.DataType;
import org.apache.spark.sql.types.DataTypes;

import zingg.client.ZFrame;
import zingg.hash.LastWord;

public class SparkLastWord extends LastWord<Dataset<Row>,Row,Column,DataType> implements UDF1<String, String>{
	
	public SparkLastWord() {
		super();
		setDataType(DataTypes.StringType);
		setReturnType(DataTypes.StringType);
		
	}

	@Override
	public Object getAs(Row r, String column) {
		return (String) r.getAs(column);
	}



	@Override
	public ZFrame<Dataset<Row>, Row, Column> apply(ZFrame<Dataset<Row>, Row, Column> ds, String column,
			String newColumn) {
		return ds.withColumn(newColumn, functions.callUDF(this.name, ds.col(column)));
	}

	public Object apply(Row r, String column) {
		return call((String) r.getAs(column));
	}

	


}
