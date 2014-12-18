# Fabric recipe for Analice.me

Run:

    cp config.yml.example config.yml

Edit `config.yml` with your variables and then run:

    ENV=hephaestus fab hephaestus

to setup a new **Hephaestus** ready to use machine.

## TODO

* Put everything in a single command.
* Add security configurations for SSH.
* Add recipes for other stuff.

## Resources

* http://code.tutsplus.com/tutorials/setting-up-a-rails-server-and-deploying-with-capistrano-on-fedora-from-scratch--net-10443
* http://stackoverflow.com/questions/15012496/ruby-resque-redis-how-to-set-up-workers-on-different-machines
* https://briandamaged.org/blog/?p=1675
* http://highscalability.com/blog/2009/11/6/product-resque-githubs-distrubuted-job-queue.html
