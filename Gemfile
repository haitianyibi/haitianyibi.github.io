# frozen_string_literal: true

source "https://rubygems.org"

# 使用 github-pages gem 来确保与 GitHub Pages 兼容
gem "github-pages", group: :jekyll_plugins

# 或者使用单独的 gems（如果您更喜欢明确控制）
# gem "jekyll", "~> 4.0"
# gem "jekyll-feed", "~> 0.12"
# gem "jekyll-sitemap", "~> 1.3"
# gem "jekyll-seo-tag", "~> 2.6"
# gem "minima", "~> 2.5"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

# Windows 平台可能需要额外的 gem
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo-data"
end