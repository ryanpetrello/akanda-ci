Akanda CI Environment
---------------------
Requires the ``ansible`` and ``passlib`` Python packages::

    $ mv jenkins/playbooks/hosts.example jenkins/playbooks/hosts

Update ``jenkins/playbooks/hosts`` with the target SSH hostname and username
for the Jenkins install and update ``jenkins/playbooks/environment.yml`` with
correct API credentials to launch VMs in external compute services.

::

    $ ./jenkins/deploy

Check the ``jenkins/playbooks/secrets`` folder for the password generated for the
`jenkins` user.
