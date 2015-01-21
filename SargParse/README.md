SargParser
====

This is just another argparser just as the python standard library offers.

Basic Examples:

```js

import SargParse
s = SargParse.SargParser()
s.addArgument('-x', type='optional', action='storeTrue', message='x factor')
s.addArgument('-y', type='optional', action='storeTrue', message='y factor')
s.addArgument('exp', message='expression')
namespace = s.parseArg()

```

There are also some advanced features like group arguments.
