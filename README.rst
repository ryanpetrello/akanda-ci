Akanda CI Environment
---------------------
Requires the ``ansible`` and ``passlib`` Python packages::

    $ mv jenkins/playbooks/hosts.example jenkins/playbooks/hosts

Update ``jenkins/playbooks/hosts`` with the target SSH hostname and username.

::

    $ ./jenkins/deploy
