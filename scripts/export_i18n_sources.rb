# Run after the normal Chinese Jekyll build. URL and destination resolution must
# use Jekyll, particularly for the historical posts without explicit permalinks.
require 'jekyll'
require 'json'
require 'fileutils'
require 'digest'
site = Jekyll::Site.new(Jekyll.configuration)
site.read
rows = site.posts.docs.select { |post| %w[post guide work].include?(post.data['layout']) }.map do |post|
  { path: post.relative_path, url: post.url, destination: post.destination(site.dest),
    source_sha256: Digest::SHA256.file(post.path).hexdigest, data: post.data }
end
FileUtils.mkdir_p('output/bilingual')
File.write('output/bilingual/posts-source.json', JSON.pretty_generate(rows))
puts "Exported #{rows.length} original article URLs."
