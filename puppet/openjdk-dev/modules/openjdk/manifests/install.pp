class openjdk::install {


# Just remember that even with -source and -dbg files you also need to do a 'dir'
# from gdb ;-)

  package { [ 'libc6-dbg', 'glibc-source', 'vim', 'nmap' ]: 
    ensure => 'present',
  }
}
