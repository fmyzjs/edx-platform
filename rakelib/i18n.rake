# --- Internationalization tasks

namespace :i18n do

  desc "Extract localizable strings from sources"
  task :extract => ["i18n:validate:gettext", "assets:coffee"] do
    command = "i18n_tool extract"
    if verbose == true
      command += " -vv"
    end
    sh(command)
  end

  desc "Compile localizable strings from sources, extracting strings first."
  task :generate => "i18n:extract" do
    cmd = "i18n_tool generate"
    sh("#{cmd}")
  end

  desc "Compile localizable strings from sources, extracting strings first, and complain if files are missing."
  task :generate_strict => "i18n:extract" do
    cmd = "i18n_tool generate"
    sh("#{cmd} --strict")
  end

  desc "Simulate international translation by generating dummy strings corresponding to source strings."
  task :dummy => "i18n:extract" do
    sh("i18n_tool dummy")
  end

  namespace :validate do

    desc "Make sure GNU gettext utilities are available"
    task :gettext do
      begin
        select_executable('xgettext')
      rescue
        msg = "Cannot locate GNU gettext utilities, which are required by django for internationalization.\n"
        msg += "(see https://docs.djangoproject.com/en/dev/topics/i18n/translation/#message-files)\n"
        msg += "Try downloading them from http://www.gnu.org/software/gettext/"
        abort(msg.red)
      end
    end

    desc "Make sure config file with username/password exists"
    task :transifex_config do
      config_file = "#{Dir.home}/.transifexrc"
      if !File.file?(config_file) or File.size(config_file)==0
        msg ="Cannot connect to Transifex, config file is missing or empty: #{config_file}\n"
        msg += "See http://help.transifex.com/features/client/#transifexrc"
        abort(msg.red)
      end
    end
  end

  namespace :transifex do
    desc "Push source strings to Transifex for translation"
    task :push => "i18n:validate:transifex_config" do
      cmd = "i18n_tool transifex"
      sh("#{cmd} push")
    end

    desc "Pull translated strings from Transifex"
    task :pull => "i18n:validate:transifex_config" do
      cmd = "i18n_tool transifex"
      sh("#{cmd} pull")
    end
  end

  # Commands for automating the process of including translations in edx-platform.
  # Will eventually be run by jenkins.
  namespace :robot do
    desc "Pull source strings, generate po and mo files, and validate"
    task :pull => ["i18n:transifex:pull", "i18n:extract", "i18n:dummy", "i18n:generate_strict"] do
      sh('git clean -fdX conf/locale')
      Rake::Task["i18n:test"].invoke
      sh('git add conf/locale')
      sh('git commit --message="Update translations (autogenerated message)" --edit')
    end

    desc "Extract new strings, and push to transifex"
    task :push => ["i18n:extract", "i18n:transifex:push"]
  end

end
