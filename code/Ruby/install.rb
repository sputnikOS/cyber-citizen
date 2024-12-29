# List of gems to be installed
required_gems = [
  { name: 'dotenv', version: nil },     # Example: Install latest version
  { name: 'shodan', version: '1.0.0' }, # Example: Install specific version
  { name: 'colorize', version: nil }
]

# Method to check if a gem is installed
def gem_installed?(name, version = nil)
  if version
    Gem::Specification.find_by_name(name, version)
  else
    Gem::Specification.find_by_name(name)
  end
  true
rescue Gem::LoadError
  false
end

# Method to install a gem
def install_gem(name, version = nil)
  if version
    system("gem install #{name} -v #{version}")
  else
    system("gem install #{name}")
  end
end

# Install required gems
required_gems.each do |gem|
  name = gem[:name]
  version = gem[:version]

  if gem_installed?(name, version)
    puts "Gem '#{name}' #{version ? "(#{version})" : ''} is already installed."
  else
    puts "Installing gem '#{name}' #{version ? "(#{version})" : ''}..."
    install_gem(name, version)
  end
end

puts "All required gems are installed!"
