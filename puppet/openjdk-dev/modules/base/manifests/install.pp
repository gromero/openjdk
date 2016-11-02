class base::install {
  package { ['sysstat']: 
    ensure => 'present',
  } 
}
