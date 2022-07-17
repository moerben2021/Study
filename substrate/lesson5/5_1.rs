# storage宏
# [frame_support::pallet]
pub mod pallet {
  // --snippet --
}

#[pallet::config]
pub trait Config: frame_system::Config {
  type Event: From<Event<Self>> + IsType<<Self as frame_system::Config>::Event>;
}

#[pallet::storage]
#[pallet::getter(fn something)]
pub type Something<T> = StorageValue<_, u32>;
