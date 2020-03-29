source "https://rubygems.org"
# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima"
gem "activesupport", ">= 4.1.11"


gem "github-pages", group: :jekyll_plugins
group :jekyll_plugins do
  gem "jekyll-feed"
  gem 'jemoji'
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem "tzinfo"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :install_if => Gem.win_platform?

