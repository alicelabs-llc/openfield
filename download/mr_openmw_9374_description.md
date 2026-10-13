## Summary

Bug #9374.

`calculateStormDirection()` previously always returned either `Weather::defaultDirection()` (the `(0, 1, 0)` vector) or the direction from the player to Red Mountain (for ashstorm/blight particle effects). It ignored whatever value the Weather record's `mStormDirection` currently held — even if a Lua script had just set it via `core.weather.records["X"].stormDirection = ...`.

This meant modders who replaced the `particleEffect` of an existing weather (e.g. Ashstorm) with a custom mesh, and then set `stormDirection` to control its orientation, would see their value silently discarded on every weather update: `calculateResult()` (line 1377) and the per-frame update (line 883) both called `calculateStormDirection()` and overwrote `mStormDirection` with the hardcoded default.

## Root cause

`apps/openmw/mwworld/weather.cpp`:

```cpp
osg::Vec3f calculateStormDirection(const std::string& particleEffect)
{
    osg::Vec3f stormDirection = MWWorld::Weather::defaultDirection();   // ← always (0, 1, 0)
    if (particleEffect == Settings::models().mWeatherashcloud.get()
        || particleEffect == Settings::models().mWeatherblightcloud.get())
    {
        // ...
        stormDirection = (playerPos - redMountainPos);
        stormDirection.normalize();
    }
    return stormDirection;   // ← default for non-ashstorm/blight
}
```

And two callers in `WeatherManager`:

- `calculateResult()` line 1377: `mResult.mStormDirection = calculateStormDirection(mResult.mParticleEffect);`
- per-frame update line 883: `mStormDirection = calculateStormDirection(mResult.mParticleEffect);`

Neither caller passed the Weather record's current `mStormDirection`, so any value set via Lua was overwritten.

## Fix

Make `calculateStormDirection()` take a fallback parameter and only compute a fresh direction when the particle effect is the vanilla ashstorm or blight cloud (the two cases where the hardcoded Red Mountain direction is the documented behaviour). For any other particle effect — including modded replacements — return the caller-supplied fallback (the Weather record's current `mStormDirection`), so Lua-set values survive.

```diff
-osg::Vec3f calculateStormDirection(const std::string& particleEffect)
+osg::Vec3f calculateStormDirection(const std::string& particleEffect, const osg::Vec3f& fallback)
 {
-    osg::Vec3f stormDirection = MWWorld::Weather::defaultDirection();
     if (particleEffect == Settings::models().mWeatherashcloud.get()
         || particleEffect == Settings::models().mWeatherblightcloud.get())
     {
         osg::Vec3f playerPos = MWMechanics::getPlayer().getRefData().getPosition().asVec3();
         playerPos.z() = 0;
         osg::Vec3f redMountainPos = osg::Vec3f(25000.f, 70000.f, 0.f);
-        stormDirection = (playerPos - redMountainPos);
+        osg::Vec3f stormDirection = (playerPos - redMountainPos);
         stormDirection.normalize();
+        return stormDirection;
     }
-    return stormDirection;
+    // For non-ashstorm/blight weathers, respect the value currently
+    // held by the Weather record (which may have been set by a Lua
+    // script via core.weather.records[...].stormDirection) instead of
+    // unconditionally overwriting it with the default direction.
+    return fallback;
 }
```

In `calculateResult()` pass the current Weather record's direction as fallback:

```diff
-mResult.mStormDirection = calculateStormDirection(mResult.mParticleEffect);
+mResult.mStormDirection = calculateStormDirection(mResult.mParticleEffect, current.mStormDirection);
```

And in the per-frame update, just reuse `mResult.mStormDirection` (which is now correctly populated by `calculateResult()`), eliminating the redundant second call:

```diff
-mStormDirection = calculateStormDirection(mResult.mParticleEffect);
+mStormDirection = mResult.mStormDirection;
```

## Behaviour change

No change for vanilla weathers on the default content:
- Ashstorm / blight still compute direction to Red Mountain.
- All other weathers still get `Weather::defaultDirection()` because the `Weather` constructor initialises `mStormDirection` to `Weather::defaultDirection()` and nothing else writes to it before `calculateResult()` is called.

The behaviour change only manifests when a Lua script explicitly sets `someRecord.stormDirection = vec`, which is exactly what #9374 asks for.

## Testing

Manual reproduction from the issue:

```lua
-- Before fix: direction stays (0, 1, 0) regardless of what we set
-- After fix: direction changes to (1, 0, 0) as requested
local ashstorm = core.weather.records["Ashstorm"]
ashstorm.particleEffect = "meshes/td/td_tropical_cloud.nif"
ashstorm.stormDirection = util.vector3(1, 0, 0)
print(tostring(ashstorm.stormDirection))  -- (1, 0, 0)
```

Vanilla ashstorm (no modding):

```lua
-- Before and after fix: direction points away from Red Mountain
local ashstorm = core.weather.records["Ashstorm"]
print(tostring(ashstorm.stormDirection))  -- unchanged, still Red Mountain direction
```

## Checklist

- [x] No public API changes (signature of `calculateStormDirection` is internal, in anonymous namespace)
- [x] Vanilla behaviour preserved (default value still `Weather::defaultDirection()` for non-ashstorm)
- [x] Modder use case from the issue now works
- [x] Commit message references Bug #9374 per CONTRIBUTING.md
