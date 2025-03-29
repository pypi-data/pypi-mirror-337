# Logs

## with timeout=1

```bash
========================================================================= short test summary info =========================================================================
FAILED tests/test_connections.py::Tests::test_hop1_dup - AssertionError: -6 != 4
FAILED tests/test_connections.py::Tests::test_hop1_multi_sched_nested21 - AssertionError: -6 != 4
================================================================ 2 failed, 107 passed in 364.54s (0:06:04) ================================================================
```

## with timeout=2

```bash
========================================================================= short test summary info =========================================================================
FAILED tests/test_connections.py::Tests::test_hop1_dup - AssertionError: -6 != 4
FAILED tests/test_connections.py::Tests::test_hop1_shared_sched_nested21 - AssertionError: -11 != 1
FAILED tests/test_services.py::Tests::test_simple_forever - AssertionError: 2 != 0
FAILED tests/test_services.py::Tests::test_simple_regular - AssertionError: 2 != 0
================================================================ 4 failed, 105 passed in 361.39s (0:06:01) ================================================================
```

## and again for repeatability

```bash
========================================================================= short test summary info =========================================================================
FAILED tests/test_connections.py::Tests::test_hop1_dup - AssertionError: -6 != 4
FAILED tests/test_connections.py::Tests::test_hop1_shared_sched_nested21 - AssertionError: -9 != 1
FAILED tests/test_services.py::Tests::test_simple_regular - AssertionError: 2 != 0
================================================================ 3 failed, 106 passed in 359.83s (0:05:59) ================================================================
```

!!!
check for the 'tick' service
was it something we have setup ourselves or what ?!?!
!!!
