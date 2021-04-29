# py_pgsql_dict_writer
Script to write python dictionaries into a PostgreSQL database.
I wrote this to work as a module for a in house monitoring solution in a TimeScale database.

## Usage
### Edit config.json
This is a JSON file, use it tell where to write:  
```
{
 "target_database": [  
  {  
  "db": "psqlmetrics",  
  "host": "localhost",  
  "user": "postgres",  
  "port": "50000",  
  "type": "pgsql12",  
  "table_prefix": "psqlmetrics.",  
  "table_suffix": ""  
  }  
 ]  
}
```
Don't have a password key/value because we have client SSL connection.
You should use it too instead of passwords.

## Include it in your scripts:
```from writetarget import target_pgsql as pgsql```

## Def dict as a variable in your own way
```
cpu_load_metrics = {  
 "hostname": "prd-superapp-01",  
 "nr_cores": "4",
 "load_pct": 67
 }
```

## Write
**Dictionary KEYS must match column names in target database,** dictionary VALUES represent the data to write

```pgsql().write('cpu_load',cpu_load_metrics)```




