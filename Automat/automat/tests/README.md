# Testing Automat

Automat is a proxy server for multiple instance. It is really unaware of the paths
implemented in the Platers, but is able to proxy different types of HTTP requests to
registered instances. 

Running these tests can be done using pytest. 

### Test files

* [test_core.py](https://github.com/RENCI-AUTOMAT/Automat-server/blob/master/Automat/automat/tests/test_core.py)

Tests proxy functionality with mock servers. Asserts responses from downstream servers are passed down.
  
* [test_registry.py](https://github.com/RENCI-AUTOMAT/Automat-server/blob/master/Automat/automat/tests/test_registry.py)

Tests registry of automat and registered endpoints expire after some time.  

