class openjdk::install {


  package { [ 'libc6-dbg', 'vim', 'nmap' ]: 
    ensure => 'present',
  }
}
