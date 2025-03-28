#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pddl" for configuration "Release"
set_property(TARGET pddl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(pddl PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "core;wrapper"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lapkt/core/lib/pddl.so"
  IMPORTED_SONAME_RELEASE "pddl.so"
  )

list(APPEND _cmake_import_check_targets pddl )
list(APPEND _cmake_import_check_files_for_pddl "${_IMPORT_PREFIX}/lapkt/core/lib/pddl.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
