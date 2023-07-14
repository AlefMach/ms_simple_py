# Logging

[Logging Official](https://docs.python.org/3/library/logging.html)

[Python Logging Levels Explained](https://www.logicmonitor.com/blog/python-logging-levels-explained)

* Logging Flow
![Logging Flow](images/logging/logging_flow.png "Logging Flow")

## code for debug of logging conf
```python
def debug_logger():
    for key, value in logging.root.manager.loggerDict.items():
        if not isinstance(value, logging.PlaceHolder):
            formatter = None
            if value.handlers and value.handlers[0].formatter:
                formatter = value.handlers[0].formatter.__dict__['_fmt']
            if value.parent.handlers and value.parent.handlers[0].formatter:
                formatter = value.parent.handlers[0].formatter.__dict__['_fmt']

            logger.error(
                f"{key, logging.getLevelName(value.level) if hasattr(value, 'level') else None, value.handlers, value.filters, value.parent.name, formatter}"  # noqa E501
            )
```
