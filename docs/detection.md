# {octicon}`pulse` Detection

## Trait detection functions

```{eval-rst}
.. automodule:: extra_platforms.detection
   :members:
   :undoc-members:
   :show-inheritance:
```

## Group detection functions

Contrary to individual trait detection functions like `is_linux()` or `is_x86_64()`, group detection functions check for membership in a collection of traits.

These functions are dynamically generated for each [group](groups.md) and test whether **at least one trait** from the group matches the current system:

<!-- group-detection-autofunction-start -->

```{eval-rst}
.. autofunction:: extra_platforms.is_all_architectures
.. autofunction:: extra_platforms.is_all_ci
.. autofunction:: extra_platforms.is_all_platforms
.. autofunction:: extra_platforms.is_all_traits
.. autofunction:: extra_platforms.is_any_arm
.. autofunction:: extra_platforms.is_any_mips
.. autofunction:: extra_platforms.is_any_sparc
.. autofunction:: extra_platforms.is_any_windows
.. autofunction:: extra_platforms.is_arch_32_bit
.. autofunction:: extra_platforms.is_arch_64_bit
.. autofunction:: extra_platforms.is_bsd
.. autofunction:: extra_platforms.is_bsd_without_macos
.. autofunction:: extra_platforms.is_ibm_mainframe
.. autofunction:: extra_platforms.is_linux
.. autofunction:: extra_platforms.is_linux_layers
.. autofunction:: extra_platforms.is_linux_like
.. autofunction:: extra_platforms.is_loongarch
.. autofunction:: extra_platforms.is_other_unix
.. autofunction:: extra_platforms.is_powerpc
.. autofunction:: extra_platforms.is_riscv
.. autofunction:: extra_platforms.is_system_v
.. autofunction:: extra_platforms.is_unix
.. autofunction:: extra_platforms.is_unix_layers
.. autofunction:: extra_platforms.is_unix_without_macos
.. autofunction:: extra_platforms.is_unknown
.. autofunction:: extra_platforms.is_webassembly
.. autofunction:: extra_platforms.is_x86
```

<!-- group-detection-autofunction-end -->
